"""Scheduled Cankaya forecast and verification workflow.

This script is designed to be run by launchd. It creates at most one forecast
per ECMWF Open Data cycle during the forecast window, verifies mature forecast
files when their target dates have reference values, and keeps aggregate metric
tables up to date.
"""

from __future__ import annotations

import argparse
import datetime as dt
import logging
import math
import subprocess
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
import s3fs

REPO_ROOT = Path(__file__).resolve().parents[1]

DEFAULT_LAT = 39.9179
DEFAULT_LON = 32.8627
LOCAL_TZ = ZoneInfo("Europe/Istanbul")

FORECAST_START = dt.date(2026, 5, 7)
FORECAST_END = dt.date(2026, 5, 14)

AUTOMATION_DIR = REPO_ROOT / "reports" / "automation"
FORECAST_DIR = AUTOMATION_DIR / "forecasts"
FORECAST_REPORT_DIR = AUTOMATION_DIR / "forecast_reports"
VERIFICATION_DIR = AUTOMATION_DIR / "verifications"
VERIFICATION_REPORT_DIR = AUTOMATION_DIR / "verification_reports"
LOG_DIR = AUTOMATION_DIR / "logs"

FIELDS = ("z500_m", "t850_c", "wind850_ms")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("cankaya_automation")


def parse_date(value: str) -> dt.date:
    return dt.date.fromisoformat(value)


def ensure_dirs() -> None:
    for path in (
        FORECAST_DIR,
        FORECAST_REPORT_DIR,
        VERIFICATION_DIR,
        VERIFICATION_REPORT_DIR,
        LOG_DIR,
    ):
        path.mkdir(parents=True, exist_ok=True)


def cycle_s3_path(init_time: pd.Timestamp) -> str:
    init_time = pd.Timestamp(init_time)
    stream = "oper" if init_time.hour in (0, 12) else "scda"
    date = init_time.strftime("%Y%m%d")
    hour = init_time.strftime("%H")
    filename = f"{date}{hour}0000-0h-{stream}-fc.grib2"
    return f"ecmwf-forecasts/{date}/{hour}z/ifs/0p25/{stream}/{filename}"


def latest_ecmwf_cycle(max_lookback_hours: int) -> pd.Timestamp:
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


def forecast_id(init_time: pd.Timestamp) -> str:
    init_time = pd.Timestamp(init_time).tz_localize(None)
    return init_time.strftime("%Y%m%dT%HZ")


def forecast_paths(init_time: pd.Timestamp) -> tuple[Path, Path]:
    fid = forecast_id(init_time)
    csv_path = FORECAST_DIR / f"cankaya_keisler_{fid}.csv"
    report_path = FORECAST_REPORT_DIR / f"cankaya_keisler_{fid}.md"
    return csv_path, report_path


def verification_paths(forecast_csv: Path) -> tuple[Path, Path]:
    fid = forecast_csv.stem.removeprefix("cankaya_keisler_")
    csv_path = VERIFICATION_DIR / f"cankaya_keisler_{fid}_verified.csv"
    report_path = VERIFICATION_REPORT_DIR / f"cankaya_keisler_{fid}_verified.md"
    return csv_path, report_path


def run_command(argv: list[str]) -> None:
    logger.info("Running: %s", " ".join(argv))
    subprocess.run(argv, cwd=REPO_ROOT, check=True)


def run_forecast_if_due(args: argparse.Namespace, today: dt.date) -> Path | None:
    if not (args.forecast_start <= today <= args.forecast_end):
        logger.info(
            "Forecast production is outside window %s..%s; today=%s",
            args.forecast_start,
            args.forecast_end,
            today,
        )
        return None

    init_time = latest_ecmwf_cycle(args.max_lookback_hours)
    csv_path, report_path = forecast_paths(init_time)
    if csv_path.exists() and report_path.exists() and not args.force_forecast:
        logger.info("Forecast already exists for init=%s: %s", init_time, csv_path)
        return csv_path

    run_command(
        [
            sys.executable,
            "scripts/05_point_weekly_forecast.py",
            "--lat",
            str(args.lat),
            "--lon",
            str(args.lon),
            "--init",
            init_time.isoformat(),
            "--days",
            str(args.days),
            "--out-csv",
            str(csv_path),
            "--out-report",
            str(report_path),
        ]
    )
    logger.info("Forecast complete for init=%s", init_time.isoformat())
    return csv_path


def forecast_target_window(forecast_csv: Path) -> tuple[pd.Timestamp, pd.Timestamp]:
    forecast = pd.read_csv(forecast_csv, usecols=["target_time", "lead_hours"])
    forecast["target_time"] = pd.to_datetime(forecast["target_time"], utc=False)
    forecast = forecast[forecast["lead_hours"] > 0]
    return forecast["target_time"].min(), forecast["target_time"].max()


def verification_ready(
    forecast_csv: Path,
    now_utc: pd.Timestamp,
    reference_lag_hours: int,
) -> tuple[bool, pd.Timestamp]:
    _first_target, last_target = forecast_target_window(forecast_csv)
    ready_after = last_target + pd.Timedelta(hours=reference_lag_hours)
    return now_utc >= ready_after, ready_after


def verify_mature_forecasts(
    args: argparse.Namespace, now_utc: pd.Timestamp
) -> list[Path]:
    verified_paths = []
    for forecast_csv in sorted(FORECAST_DIR.glob("cankaya_keisler_*.csv")):
        out_csv, out_report = verification_paths(forecast_csv)
        if out_csv.exists() and out_report.exists() and not args.force_verify:
            logger.info("Verification already exists: %s", out_csv)
            verified_paths.append(out_csv)
            continue

        ready, ready_after = verification_ready(
            forecast_csv,
            now_utc=now_utc,
            reference_lag_hours=args.reference_lag_hours,
        )
        if not ready and not args.force_verify:
            logger.info(
                "Forecast is not mature for verification yet: %s; ready after %s UTC",
                forecast_csv,
                ready_after,
            )
            continue

        run_command(
            [
                sys.executable,
                "scripts/06_verify_point_forecast.py",
                "--forecast-csv",
                str(forecast_csv),
                "--lat",
                str(args.lat),
                "--lon",
                str(args.lon),
                "--out-csv",
                str(out_csv),
                "--out-report",
                str(out_report),
            ]
        )
        verified_paths.append(out_csv)
        logger.info("Verification complete: %s", out_csv)
    return verified_paths


def _clean_numeric(series: pd.Series) -> pd.Series:
    return pd.to_numeric(series, errors="coerce")


def _rmse(values: pd.Series) -> float:
    values = _clean_numeric(values).dropna()
    if values.empty:
        return math.nan
    return float(np.sqrt(np.mean(values**2)))


def _mae(values: pd.Series) -> float:
    values = _clean_numeric(values).dropna()
    if values.empty:
        return math.nan
    return float(np.mean(np.abs(values)))


def _corr(left: pd.Series, right: pd.Series) -> float:
    left = _clean_numeric(left)
    right = _clean_numeric(right)
    mask = left.notna() & right.notna()
    if int(mask.sum()) < 2:
        return math.nan
    if float(left[mask].std()) == 0.0 or float(right[mask].std()) == 0.0:
        return math.nan
    return float(left[mask].corr(right[mask]))


def load_scored_verifications() -> pd.DataFrame:
    frames = []
    for verified_csv in sorted(VERIFICATION_DIR.glob("cankaya_keisler_*_verified.csv")):
        fid = verified_csv.stem.removeprefix("cankaya_keisler_").removesuffix(
            "_verified"
        )
        forecast_csv = FORECAST_DIR / f"cankaya_keisler_{fid}.csv"
        if not forecast_csv.exists():
            logger.warning("Missing source forecast for verification: %s", verified_csv)
            continue

        verified = pd.read_csv(verified_csv)
        verified["forecast_id"] = fid
        verified["target_time"] = pd.to_datetime(verified["target_time"], utc=False)

        source = pd.read_csv(forecast_csv)
        source_initial = source[source["lead_hours"] == 0]
        if source_initial.empty:
            logger.warning("Missing lead_hours=0 row in forecast: %s", forecast_csv)
            continue
        initial = source_initial.iloc[0]
        for field in FIELDS:
            verified[f"persistence_{field}"] = float(initial[f"pred_{field}"])

        required = [f"actual_{field}" for field in FIELDS]
        verified = verified.dropna(subset=required)
        if not verified.empty:
            frames.append(verified)

    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


def metric_row(df: pd.DataFrame, field: str) -> dict[str, float | int | str]:
    pred = _clean_numeric(df[f"pred_{field}"])
    actual = _clean_numeric(df[f"actual_{field}"])
    persistence = _clean_numeric(df[f"persistence_{field}"])
    mask = pred.notna() & actual.notna()
    err = pred[mask] - actual[mask]
    persistence_err = persistence[mask] - actual[mask]

    actual_range = (
        float(actual[mask].max() - actual[mask].min()) if mask.any() else math.nan
    )
    mae = _mae(err)
    rmse = _rmse(err)
    persistence_rmse = _rmse(persistence_err)
    if math.isfinite(actual_range) and actual_range > 0 and math.isfinite(mae):
        range_accuracy_pct = max(0.0, min(100.0, 100.0 * (1.0 - mae / actual_range)))
    else:
        range_accuracy_pct = math.nan
    if math.isfinite(persistence_rmse) and persistence_rmse > 0 and math.isfinite(rmse):
        skill_vs_persistence_pct = 100.0 * (1.0 - rmse / persistence_rmse)
    else:
        skill_vs_persistence_pct = math.nan

    return {
        "field": field,
        "n": int(mask.sum()),
        "mae": mae,
        "rmse": rmse,
        "bias": float(np.nanmean(err)) if not err.empty else math.nan,
        "corr": _corr(pred, actual),
        "actual_range": actual_range,
        "range_accuracy_pct": range_accuracy_pct,
        "persistence_rmse": persistence_rmse,
        "skill_vs_persistence_pct": skill_vs_persistence_pct,
    }


def build_metric_tables(scored: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame]:
    overall = pd.DataFrame([metric_row(scored, field) for field in FIELDS])

    by_forecast_rows = []
    for fid, group in scored.groupby("forecast_id", sort=True):
        row: dict[str, float | int | str] = {
            "forecast_id": fid,
            "init_time": str(group["init_time"].iloc[0]),
            "rows_scored": int(len(group)),
            "target_start": group["target_time"].min().isoformat(),
            "target_end": group["target_time"].max().isoformat(),
        }
        for field in FIELDS:
            err = _clean_numeric(group[f"pred_{field}"]) - _clean_numeric(
                group[f"actual_{field}"]
            )
            row[f"{field}_mae"] = _mae(err)
            row[f"{field}_rmse"] = _rmse(err)
        by_forecast_rows.append(row)

    by_forecast = pd.DataFrame(by_forecast_rows)
    return overall, by_forecast


def write_accuracy_summary(now_local: dt.datetime) -> None:
    scored = load_scored_verifications()
    summary_csv = AUTOMATION_DIR / "accuracy_summary.csv"
    by_forecast_csv = AUTOMATION_DIR / "accuracy_by_forecast.csv"
    summary_md = AUTOMATION_DIR / "accuracy_summary.md"

    forecast_count = len(list(FORECAST_DIR.glob("cankaya_keisler_*.csv")))
    verification_count = len(
        list(VERIFICATION_DIR.glob("cankaya_keisler_*_verified.csv"))
    )

    if scored.empty:
        content = f"""# Cankaya Automated Forecast Accuracy

- Last update: `{now_local.isoformat()}`.
- Forecast files: `{forecast_count}`.
- Verified forecast files: `{verification_count}`.
- Status: no mature verified forecast rows are available yet.

The job will update this file after forecast target dates have reference values.
"""
        summary_md.write_text(content, encoding="utf-8")
        logger.info("No scored verification rows yet; wrote %s", summary_md)
        return

    overall, by_forecast = build_metric_tables(scored)
    overall.to_csv(summary_csv, index=False)
    by_forecast.to_csv(by_forecast_csv, index=False)

    content = f"""# Cankaya Automated Forecast Accuracy

- Last update: `{now_local.isoformat()}`.
- Forecast files: `{forecast_count}`.
- Verified forecast files: `{verification_count}`.
- Scored rows: `{len(scored)}`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.
- Percentage column: range-normalized diagnostic only; MAE, RMSE, bias, corr, and persistence skill are the primary metrics.

## Overall Metrics

{overall.to_markdown(index=False)}

## By Forecast Run

{by_forecast.to_markdown(index=False)}
"""
    summary_md.write_text(content, encoding="utf-8")
    logger.info("Wrote accuracy summary: %s", summary_md)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run scheduled Cankaya forecast and verification workflow."
    )
    parser.add_argument("--lat", type=float, default=DEFAULT_LAT)
    parser.add_argument("--lon", type=float, default=DEFAULT_LON)
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--forecast-start", type=parse_date, default=FORECAST_START)
    parser.add_argument("--forecast-end", type=parse_date, default=FORECAST_END)
    parser.add_argument("--reference-lag-hours", type=int, default=24)
    parser.add_argument("--max-lookback-hours", type=int, default=120)
    parser.add_argument("--force-forecast", action="store_true")
    parser.add_argument("--force-verify", action="store_true")
    args = parser.parse_args()

    ensure_dirs()
    now_local = dt.datetime.now(LOCAL_TZ)
    now_utc = pd.Timestamp.utcnow().tz_localize(None)
    logger.info("Automation run started at %s", now_local.isoformat())

    errors = []
    try:
        run_forecast_if_due(args, today=now_local.date())
    except Exception as exc:  # noqa: BLE001 - keep launchd run moving to verify.
        logger.exception("Forecast step failed")
        errors.append(exc)

    try:
        verify_mature_forecasts(args, now_utc=now_utc)
        write_accuracy_summary(now_local)
    except Exception as exc:  # noqa: BLE001 - report launchd failure clearly.
        logger.exception("Verification or summary step failed")
        errors.append(exc)

    if errors:
        raise SystemExit(1)
    logger.info("Automation run finished")


if __name__ == "__main__":
    main()
