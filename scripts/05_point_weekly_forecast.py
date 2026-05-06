"""Create a 7-day point forecast from the latest ECMWF Open Data analysis.

The Keisler 2022 model predicts pressure-level fields. This script samples those
fields at the nearest 1-degree grid point for a requested location and writes a
CSV plus a small Markdown report.
"""

from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

import jax
import numpy as np
import pandas as pd
import s3fs

from keisler_2022.config import Config
from keisler_2022.io import GRAVITY, load_ecmwf_open_data
from keisler_2022.runner import Runner, levels, varnames

DEFAULT_LAT = 39.9179
DEFAULT_LON = 32.8627

FIELDS = {
    "z500_m": ("geopotential", 500),
    "t850_c": ("temperature", 850),
    "u850_ms": ("u_component_of_wind", 850),
    "v850_ms": ("v_component_of_wind", 850),
    "q850_gkg": ("specific_humidity", 850),
}

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("point_weekly_forecast")


def cycle_s3_path(init_time: pd.Timestamp) -> str:
    init_time = pd.Timestamp(init_time)
    stream = "oper" if init_time.hour in (0, 12) else "scda"
    date = init_time.strftime("%Y%m%d")
    hour = init_time.strftime("%H")
    filename = f"{date}{hour}0000-0h-{stream}-fc.grib2"
    return f"ecmwf-forecasts/{date}/{hour}z/ifs/0p25/{stream}/{filename}"


def latest_ecmwf_cycle(max_lookback_hours: int = 120) -> pd.Timestamp:
    fs = s3fs.S3FileSystem(anon=True)
    now = pd.Timestamp.utcnow().floor("h")
    checked: set[pd.Timestamp] = set()
    for hours_back in range(0, max_lookback_hours + 1, 6):
        candidate = (now - pd.Timedelta(hours=hours_back)).floor("12h")
        candidate = pd.Timestamp(candidate).tz_localize(None)
        if candidate in checked:
            continue
        checked.add(candidate)
        if fs.exists(cycle_s3_path(candidate)):
            return candidate
    raise RuntimeError("Could not find an ECMWF Open Data 00/12Z cycle")


def nearest_grid(lat: float, lon: float) -> tuple[int, float, float]:
    lat_values = np.arange(90, -90.1, -1.0)
    lon_values = np.arange(0, 360, 1.0)
    lon_360 = lon % 360
    lat_idx = int(np.argmin(np.abs(lat_values - lat)))
    lon_idx = int(np.argmin(np.abs(lon_values - lon_360)))
    node_idx = lat_idx * len(lon_values) + lon_idx
    return node_idx, float(lat_values[lat_idx]), float(lon_values[lon_idx])


def channel_index(var_name: str, level: int) -> int:
    return varnames.index(var_name) * len(levels) + levels.index(level)


def convert_value(name: str, value: float) -> float:
    if name == "z500_m":
        return value / GRAVITY
    if name == "t850_c":
        return value - 273.15
    if name == "q850_gkg":
        return value * 1000.0
    return value


def extract_from_channels(channels: np.ndarray) -> dict[str, float]:
    values = {}
    for name, (var_name, level) in FIELDS.items():
        raw = float(channels[channel_index(var_name, level)])
        values[name] = convert_value(name, raw)
    values["wind850_ms"] = float(np.hypot(values["u850_ms"], values["v850_ms"]))
    return values


def write_report(
    path: Path,
    df: pd.DataFrame,
    init_time: pd.Timestamp,
    requested_lat: float,
    requested_lon: float,
    grid_lat: float,
    grid_lon: float,
    runtime_seconds: float,
) -> None:
    daily = df[df["lead_hours"] % 24 == 0].copy()
    content = f"""# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `{requested_lat}`, longitude `{requested_lon}`.
- Nearest model grid point: latitude `{grid_lat}`, longitude `{grid_lon}`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `{init_time.isoformat()}` UTC.
- Forecast range: `{df["target_time"].iloc[0]}` to `{df["target_time"].iloc[-1]}`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `{runtime_seconds:.1f}s`.

## Daily Rows

{daily.to_markdown(index=False)}

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a 7-day point forecast.")
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT)
    parser.add_argument("--lon", type=float, default=DEFAULT_LON)
    parser.add_argument("--init", default="latest", help="'latest' or ISO time")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--out-csv", default="reports/cankaya_next_7d_forecast.csv")
    parser.add_argument("--out-report", default="reports/cankaya_next_7d_forecast.md")
    args = parser.parse_args()

    total_start = time.time()
    init_time = (
        latest_ecmwf_cycle() if args.init == "latest" else pd.Timestamp(args.init)
    )
    init_time = pd.Timestamp(init_time).tz_localize(None)
    n_steps = args.days * 4

    node_idx, grid_lat, grid_lon = nearest_grid(args.lat, args.lon)
    logger.info(
        "Using init=%s, nearest grid lat=%.1f lon=%.1f node=%d",
        init_time.isoformat(),
        grid_lat,
        grid_lon,
        node_idx,
    )

    logger.info("Loading ECMWF Open Data initial state")
    ds_init = load_ecmwf_open_data(init_time).load()

    devices = jax.devices()
    logger.info("JAX devices: %s", devices)
    if all(device.device_kind == "cpu" for device in devices):
        logger.warning("Running on CPU only.")

    runner = Runner(verbose=False, config=Config())
    prep = runner.prepare(ds_init, n_steps=n_steps)
    net_apply = jax.jit(prep.transformed.apply)
    graphs = prep.graphs

    records = []
    initial_node = np.asarray(prep.initial_data[node_idx])
    initial_values = extract_from_channels(
        initial_node * runner.normalizer["stds"] + runner.normalizer["means"]
    )
    records.append(
        {
            "init_time": init_time.isoformat(),
            "target_time": init_time.isoformat(),
            "lead_hours": 0,
            "lead_days": 0.0,
            "grid_lat": grid_lat,
            "grid_lon": grid_lon,
            **{f"pred_{k}": v for k, v in initial_values.items()},
        }
    )

    for step_idx in range(n_steps):
        graphs, i_step = net_apply(prep.params, graphs, step_idx)
        step_number = int(i_step)
        target_time = init_time + pd.Timedelta(hours=6 * step_number)

        node_norm = np.asarray(graphs["e"].nodes["data"][node_idx])
        node_phys = node_norm * runner.normalizer["stds"] + runner.normalizer["means"]
        values = extract_from_channels(node_phys)
        records.append(
            {
                "init_time": init_time.isoformat(),
                "target_time": target_time.isoformat(),
                "lead_hours": 6 * step_number,
                "lead_days": step_number / 4,
                "grid_lat": grid_lat,
                "grid_lon": grid_lon,
                **{f"pred_{k}": v for k, v in values.items()},
            }
        )
        if step_number % 4 == 0:
            logger.info("Forecasted +%dh/%dd", 6 * step_number, step_number // 4)

    df = pd.DataFrame.from_records(records)
    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    logger.info("Wrote CSV to %s", out_csv)

    out_report = Path(args.out_report)
    write_report(
        out_report,
        df,
        init_time,
        args.lat,
        args.lon,
        grid_lat,
        grid_lon,
        time.time() - total_start,
    )
    logger.info("Wrote report to %s", out_report)


if __name__ == "__main__":
    main()
