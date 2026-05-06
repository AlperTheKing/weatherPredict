"""Point hindcast comparison for the Keisler 2022 GNN model.

This script samples an autoregressive Keisler forecast at one location and
compares daily lead times against ERA5 truth at the nearest 1-degree grid point.

It compares model-native pressure-level fields, not surface station weather.

Example:
    uv run --extra scripts scripts/04_point_hindcast.py \
        --start 2026-01-01T00 --requested-end 2026-05-06 \
        --out-csv /tmp/cankaya_2026_keisler_daily.csv \
        --out-report reports/cankaya_2026_hindcast.md
"""

from __future__ import annotations

import argparse
import json
import logging
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import jax
import numpy as np
import pandas as pd
import xarray as xr

from keisler_2022.config import Config
from keisler_2022.io import GRAVITY, load_arco_era5
from keisler_2022.runner import Runner, levels, varnames

ERA5_URL = "gs://gcp-public-data-arco-era5/ar/full_37-1h-0p25deg-chunk-1.zarr-v3"

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
logger = logging.getLogger("point_hindcast")


def channel_index(var_name: str, level: int) -> int:
    return varnames.index(var_name) * len(levels) + levels.index(level)


def nearest_grid(lat: float, lon: float) -> tuple[int, int, int, float, float]:
    lat_values = np.arange(90, -90.1, -1.0)
    lon_values = np.arange(0, 360, 1.0)
    lon_360 = lon % 360
    lat_idx = int(np.argmin(np.abs(lat_values - lat)))
    lon_idx = int(np.argmin(np.abs(lon_values - lon_360)))
    node_idx = lat_idx * len(lon_values) + lon_idx
    return (
        node_idx,
        lat_idx,
        lon_idx,
        float(lat_values[lat_idx]),
        float(lon_values[lon_idx]),
    )


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


def load_truth_point(
    times: pd.DatetimeIndex,
    grid_lat: float,
    grid_lon: float,
) -> tuple[xr.Dataset, pd.Timestamp]:
    logger.info("Opening ERA5 ARCO metadata")
    ds = xr.open_dataset(ERA5_URL, engine="zarr", decode_timedelta=False)
    valid_stop = pd.Timestamp(ds.attrs["valid_time_stop_era5t"])

    needed_vars = sorted({var_name for var_name, _ in FIELDS.values()})
    needed_levels = sorted({level for _, level in FIELDS.values()})

    logger.info("Loading ERA5 truth point for %d daily times", len(times))
    truth = (
        ds[needed_vars]
        .sel(level=needed_levels)
        .sel(time=times, latitude=grid_lat, longitude=grid_lon, method="nearest")
        .astype(np.float32)
        .load()
    )
    return truth, valid_stop


def load_openmeteo_ifs_truth(
    times: pd.DatetimeIndex,
    lat: float,
    lon: float,
) -> tuple[pd.DataFrame, dict[str, float | str]]:
    start_date = times[0].date().isoformat()
    end_date = times[-1].date().isoformat()
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": start_date,
        "end_date": end_date,
        "hourly": ",".join(
            [
                "temperature_850hPa",
                "geopotential_height_500hPa",
                "wind_speed_850hPa",
            ]
        ),
        "timezone": "UTC",
        "models": "ecmwf_ifs025",
    }
    url = "https://historical-forecast-api.open-meteo.com/v1/forecast?" + urlencode(
        params
    )
    logger.info(
        "Loading Open-Meteo ECMWF IFS reference: %s to %s", start_date, end_date
    )
    with urlopen(url, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))

    hourly = payload["hourly"]
    df = pd.DataFrame(
        {
            "time": pd.to_datetime(hourly["time"], utc=False),
            "actual_t850_c": hourly["temperature_850hPa"],
            "actual_z500_m": hourly["geopotential_height_500hPa"],
            "actual_wind850_ms": np.asarray(hourly["wind_speed_850hPa"], dtype=float)
            / 3.6,
        }
    )
    df = df.set_index("time").sort_index()
    df = df.loc[times]
    meta: dict[str, float | str] = {
        "latitude": float(payload["latitude"]),
        "longitude": float(payload["longitude"]),
        "source": "Open-Meteo historical-forecast ECMWF IFS 0.25",
    }
    return df, meta


def truth_values(truth: xr.Dataset, when: pd.Timestamp) -> dict[str, float]:
    values = {}
    for name, (var_name, level) in FIELDS.items():
        raw = float(truth[var_name].sel(time=when, level=level).item())
        values[name] = convert_value(name, raw)
    values["wind850_ms"] = float(np.hypot(values["u850_ms"], values["v850_ms"]))
    return values


def openmeteo_truth_values(truth: pd.DataFrame, when: pd.Timestamp) -> dict[str, float]:
    row = truth.loc[when]
    return {
        "z500_m": float(row["actual_z500_m"]),
        "t850_c": float(row["actual_t850_c"]),
        "wind850_ms": float(row["actual_wind850_ms"]),
    }


def metric_rows(df: pd.DataFrame) -> list[dict[str, float | str]]:
    rows: list[dict[str, float | str]] = []
    for name in ["z500_m", "t850_c", "u850_ms", "v850_ms", "wind850_ms", "q850_gkg"]:
        if f"pred_{name}" not in df or f"actual_{name}" not in df:
            continue
        err = df[f"pred_{name}"] - df[f"actual_{name}"]
        pred = df[f"pred_{name}"]
        actual = df[f"actual_{name}"]
        corr = float(pred.corr(actual)) if len(df) > 1 else float("nan")
        rows.append(
            {
                "field": name,
                "mae": float(np.mean(np.abs(err))),
                "rmse": float(np.sqrt(np.mean(err**2))),
                "bias": float(np.mean(err)),
                "corr": corr,
            }
        )
    return rows


def format_metrics(rows: list[dict[str, float | str]]) -> str:
    lines = [
        "| Field | MAE | RMSE | Bias | Corr |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for row in rows:
        lines.append(
            f"| {row['field']} | {row['mae']:.4f} | {row['rmse']:.4f} | "
            f"{row['bias']:.4f} | {row['corr']:.4f} |"
        )
    return "\n".join(lines)


def write_report(
    path: Path,
    args: argparse.Namespace,
    grid_lat: float,
    grid_lon: float,
    valid_stop: pd.Timestamp,
    truth_meta: dict[str, float | str],
    df: pd.DataFrame,
    metrics: list[dict[str, float | str]],
    total_seconds: float,
) -> None:
    requested_end = pd.Timestamp(args.requested_end).normalize()
    if args.truth_source == "openmeteo-ifs":
        unavailable_note = "None within the requested range."
    elif valid_stop.normalize() >= requested_end:
        unavailable_note = "None within the requested range."
    else:
        unavailable_note = (
            f"ERA5T truth stops at {valid_stop.date()}, so dates after that "
            f"through requested end {requested_end.date()} were not scored."
        )

    content = f"""# Çankaya 2026 Keisler Point Hindcast

This report compares a Keisler 2022 autoregressive forecast against a
pressure-level reference source for the nearest 1-degree grid point to Çankaya,
Ankara.

Important limitation: this is not surface station weather. The Keisler model
predicts pressure-level atmospheric fields, so the comparison is restricted to
overlapping pressure-level reference variables.

## Scope

- Requested location: latitude `{args.lat}`, longitude `{args.lon}`.
- Nearest model grid point: latitude `{grid_lat}`, longitude `{grid_lon}`.
- Forecast initialization: `{pd.Timestamp(args.start).isoformat()}`.
- Scored daily target range: `{df["target_time"].iloc[0]}` to `{df["target_time"].iloc[-1]}`.
- Forecast style: one autoregressive run sampled every 24 hours.
- Reference source: `{truth_meta["source"]}`.
- Reference location/grid: latitude `{truth_meta["latitude"]}`, longitude `{truth_meta["longitude"]}`.
- Requested end date: `{pd.Timestamp(args.requested_end).date()}`.
- Unavailable truth: {unavailable_note}
- Rows scored: `{len(df)}`.
- Runtime: `{total_seconds:.1f}s`.

## Accuracy

{format_metrics(metrics)}

## First Rows

{df.head(10).to_markdown(index=False)}

## Last Rows

{df.tail(10).to_markdown(index=False)}
"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Compare a point Keisler forecast against ERA5 truth."
    )
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT)
    parser.add_argument("--lon", type=float, default=DEFAULT_LON)
    parser.add_argument("--start", default="2026-01-01T00")
    parser.add_argument("--requested-end", default="2026-05-06")
    parser.add_argument("--out-csv", default="/tmp/cankaya_2026_keisler_daily.csv")
    parser.add_argument("--out-report", default="reports/cankaya_2026_hindcast.md")
    parser.add_argument(
        "--truth-source",
        choices=["openmeteo-ifs", "era5-arco"],
        default="openmeteo-ifs",
        help=(
            "Reference source. openmeteo-ifs is fast and covers the requested "
            "current date; era5-arco is model-native ERA5T but slow for point "
            "series because the public Zarr is spatially chunked."
        ),
    )
    parser.add_argument(
        "--cache-init",
        action="store_true",
        help="Cache the initial ERA5 state under /tmp.",
    )
    args = parser.parse_args()

    total_start = time.time()
    start = pd.Timestamp(args.start)
    requested_end = pd.Timestamp(args.requested_end).normalize()
    if start.hour % 6 != 0:
        raise ValueError("start must be aligned to a 6-hour forecast cycle")

    node_idx, _, _, grid_lat, grid_lon = nearest_grid(args.lat, args.lon)
    logger.info(
        "Using nearest grid point lat=%.1f lon=%.1f node=%d",
        grid_lat,
        grid_lon,
        node_idx,
    )

    first_target = start + pd.Timedelta(days=1)

    if args.truth_source == "era5-arco":
        meta = xr.open_dataset(ERA5_URL, engine="zarr", decode_timedelta=False)
        valid_stop = pd.Timestamp(meta.attrs["valid_time_stop_era5t"]).normalize()
        truth_end = min(requested_end, valid_stop)
        if truth_end < first_target:
            raise ValueError(
                f"No ERA5 truth available after start; truth_end={truth_end}"
            )
    else:
        valid_stop = requested_end
        truth_end = requested_end

    target_times = pd.date_range(first_target, truth_end, freq="24h")
    n_days = len(target_times)
    n_steps = n_days * 4
    logger.info(
        "Scoring %d daily +24h samples through %s (%d six-hour steps)",
        n_days,
        truth_end.date(),
        n_steps,
    )

    if args.truth_source == "era5-arco":
        truth, valid_stop_raw = load_truth_point(target_times, grid_lat, grid_lon)
        truth_meta: dict[str, float | str] = {
            "latitude": grid_lat,
            "longitude": grid_lon,
            "source": "ERA5 reanalysis/ERA5T via Google ARCO",
        }
    else:
        truth, truth_meta = load_openmeteo_ifs_truth(target_times, args.lat, args.lon)
        valid_stop_raw = valid_stop

    logger.info("Loading initial model state for %s", start.isoformat())
    init_load_start = time.time()
    ds_init = load_arco_era5(start, cache=args.cache_init).load()
    logger.info("Initial state loaded in %.1fs", time.time() - init_load_start)

    devices = jax.devices()
    logger.info("JAX devices: %s", devices)
    if all(device.device_kind == "cpu" for device in devices):
        logger.warning("Running on CPU only.")

    runner = Runner(verbose=False, config=Config())
    prep = runner.prepare(ds_init, n_steps=n_steps)
    net_apply = jax.jit(prep.transformed.apply)
    graphs = prep.graphs

    records = []
    forecast_start = time.time()
    for step_idx in range(n_steps):
        graphs, i_step = net_apply(prep.params, graphs, step_idx)
        step_number = int(i_step)
        if step_number % 4 != 0:
            continue

        target_time = start + pd.Timedelta(hours=6 * step_number)
        node_norm = np.asarray(graphs["e"].nodes["data"][node_idx])
        node_phys = node_norm * runner.normalizer["stds"] + runner.normalizer["means"]
        pred = extract_from_channels(node_phys)
        if args.truth_source == "era5-arco":
            actual = truth_values(truth, target_time)
        else:
            actual = openmeteo_truth_values(truth, target_time)

        record = {
            "target_time": target_time.isoformat(),
            "lead_days": step_number / 4,
            "grid_lat": grid_lat,
            "grid_lon": grid_lon,
        }
        for name in pred:
            record[f"pred_{name}"] = pred[name]
        for name in actual:
            record[f"actual_{name}"] = actual[name]
            record[f"error_{name}"] = pred[name] - actual[name]
        records.append(record)

        if len(records) % 10 == 0 or len(records) == n_days:
            logger.info("Scored %d/%d daily targets", len(records), n_days)

    logger.info("Forecast/scoring loop finished in %.1fs", time.time() - forecast_start)

    df = pd.DataFrame.from_records(records)
    metrics = metric_rows(df)

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_csv, index=False)
    logger.info("Wrote CSV to %s", out_csv)

    out_report = Path(args.out_report)
    write_report(
        out_report,
        args,
        grid_lat,
        grid_lon,
        valid_stop_raw,
        truth_meta,
        df,
        metrics,
        time.time() - total_start,
    )
    logger.info("Wrote report to %s", out_report)
    print(format_metrics(metrics))


if __name__ == "__main__":
    main()
