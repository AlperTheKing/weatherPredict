"""Verify a point forecast CSV after reference values become available."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen

import numpy as np
import pandas as pd


def load_openmeteo_reference(times: pd.Series, lat: float, lon: float) -> pd.DataFrame:
    dt = pd.to_datetime(times)
    params = {
        "latitude": lat,
        "longitude": lon,
        "start_date": dt.min().date().isoformat(),
        "end_date": dt.max().date().isoformat(),
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
    with urlopen(url, timeout=120) as response:
        payload = json.loads(response.read().decode("utf-8"))

    hourly = payload["hourly"]
    ref = pd.DataFrame(
        {
            "target_time": pd.to_datetime(hourly["time"], utc=False),
            "actual_t850_c": hourly["temperature_850hPa"],
            "actual_z500_m": hourly["geopotential_height_500hPa"],
            "actual_wind850_ms": np.asarray(hourly["wind_speed_850hPa"], dtype=float)
            / 3.6,
        }
    )
    return ref


def metrics(df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for name in ["z500_m", "t850_c", "wind850_ms"]:
        err = df[f"pred_{name}"] - df[f"actual_{name}"]
        rows.append(
            {
                "field": name,
                "n": int(err.notna().sum()),
                "mae": float(np.nanmean(np.abs(err))),
                "rmse": float(np.sqrt(np.nanmean(err**2))),
                "bias": float(np.nanmean(err)),
                "corr": float(df[f"pred_{name}"].corr(df[f"actual_{name}"])),
            }
        )
    return pd.DataFrame(rows)


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify a point forecast CSV.")
    parser.add_argument("--forecast-csv", required=True)
    parser.add_argument("--lat", type=float, default=39.9179)
    parser.add_argument("--lon", type=float, default=32.8627)
    parser.add_argument("--out-csv", default="reports/cankaya_next_7d_verified.csv")
    parser.add_argument("--out-report", default="reports/cankaya_next_7d_verified.md")
    args = parser.parse_args()

    forecast = pd.read_csv(args.forecast_csv)
    forecast["target_time"] = pd.to_datetime(forecast["target_time"], utc=False)
    forecast = forecast[forecast["lead_hours"] > 0].copy()

    ref = load_openmeteo_reference(forecast["target_time"], args.lat, args.lon)
    merged = forecast.merge(ref, on="target_time", how="left")
    for name in ["z500_m", "t850_c", "wind850_ms"]:
        merged[f"error_{name}"] = merged[f"pred_{name}"] - merged[f"actual_{name}"]

    scored = merged.dropna(
        subset=["actual_z500_m", "actual_t850_c", "actual_wind850_ms"]
    )
    metric_df = metrics(scored)

    out_csv = Path(args.out_csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    merged.to_csv(out_csv, index=False)

    out_report = Path(args.out_report)
    content = f"""# Çankaya 7-Day Forecast Verification

- Forecast CSV: `{args.forecast_csv}`.
- Rows with reference values: `{len(scored)}` / `{len(merged)}`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

{metric_df.to_markdown(index=False)}
"""
    out_report.parent.mkdir(parents=True, exist_ok=True)
    out_report.write_text(content, encoding="utf-8")

    print(metric_df.to_markdown(index=False))


if __name__ == "__main__":
    main()
