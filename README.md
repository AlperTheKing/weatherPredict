# WeatherPredict

This repository vendors the public Keisler 2022 graph neural network weather
forecasting implementation and keeps a local validation record for this machine.

The imported model is described in
[Forecasting Global Weather with Graph Neural Networks](https://arxiv.org/abs/2202.07575).
It uses an encoder/processor/decoder GNN over ERA5 latitude/longitude fields and
an H3 mesh, then rolls the 6-hour model forward autoregressively for multi-day
forecasts.

## Imported Source

- Upstream repository: <https://github.com/rkeisler/keisler-2022>
- Imported commit: `d46ba88e49ed5f90f3247e3c39f3fdc1e6f6b78a`
- Upstream README copy: [README.upstream.md](README.upstream.md)
- CLI entrypoint: `forecast.py`
- Python package: `keisler_2022`

This README intentionally does not claim current state-of-the-art status. The
goal is to make the Keisler 2022 implementation runnable, benchmark it locally,
and record measured accuracy and runtime in [VALIDATION.md](VALIDATION.md).

## Setup

Prerequisites:

- Python 3.10+
- `uv`
- Network access for package installation and ERA5 or ECMWF input data

CPU environment:

```bash
uv sync --python 3.11 --frozen --extra scripts --extra opendata
uv run python -c "import jax; print(jax.__version__, jax.devices())"
```

The repository includes `.python-version` with `3.11`. On this machine, letting
`uv` choose Python 3.14 caused `h3==3.7.7` to build from source and fail under a
newer CMake policy.

Apple Metal probe, experimental:

```bash
uv pip install jax-metal
ENABLE_PJRT_COMPATIBILITY=1 uv run python -c "import jax; print(jax.devices()); print(jax.numpy.arange(10))"
```

Local result on Apple M4 Max: `jax-metal==0.1.1` exposed `[METAL(id=0)]`, but a
basic `jnp.arange(10)` failed with a StableHLO/XLA runtime error. Keep
`jax-metal` uninstalled for the stable CPU path unless retrying Metal.

NVIDIA CUDA follows the upstream path:

```bash
uv sync --frozen --extra cuda12 --extra scripts --extra opendata
```

## Running A Forecast

ERA5 historical initialization via Google ARCO:

```bash
uv run forecast.py --init 2020-01-01T00 --steps 40 --timing --out /tmp/keisler_10d_cpu.nc
```

Recent ECMWF Open Data initialization:

```bash
uv run --extra opendata forecast.py --init 2026-02-15T00 --steps 20 --input opendata
```

`steps` are 6-hour forecast steps, so `--steps 40` is a 10-day forecast.

## Validation

The local validation sequence is:

```bash
uv run pytest -m "not network"
uv run pytest tests/test_runner.py::test_two_steps_regression
uv run --extra scripts scripts/01_evaluation.py --init 2020-01-01T00 --steps 12 --fig /tmp/era5_eval_q850.png
uv run --extra scripts scripts/01_evaluation.py --init 2020-01-01T00 --steps 1 --fig /tmp/era5_eval_q850_1step.png
uv run forecast.py --init 2020-01-01T00 --steps 40 --timing --out /tmp/keisler_10d_cpu.nc
```

Results, failures, backend status, and timing are recorded in
[VALIDATION.md](VALIDATION.md).

## Point Hindcast

For a local pressure-level comparison at Çankaya, Ankara:

```bash
uv run --extra scripts scripts/04_point_hindcast.py \
  --truth-source openmeteo-ifs \
  --start 2026-01-01T00 \
  --requested-end 2026-05-06 \
  --out-csv reports/cankaya_2026_keisler_daily.csv \
  --out-report reports/cankaya_2026_hindcast.md \
  --cache-init
```

This produces a daily autoregressive point comparison for `T850`, `Z500`, and
850 hPa wind speed. It is not a surface station forecast.

## Next 7-Day Point Forecast

To create a forward-looking 7-day Çankaya pressure-level forecast from the latest
available ECMWF Open Data analysis:

```bash
uv run --extra opendata scripts/05_point_weekly_forecast.py \
  --init latest \
  --days 7 \
  --out-csv reports/cankaya_next_7d_forecast.csv \
  --out-report reports/cankaya_next_7d_forecast.md
```

After the target dates have reference values available, verify the forecast:

```bash
uv run --extra scripts scripts/06_verify_point_forecast.py \
  --forecast-csv reports/cankaya_next_7d_forecast.csv \
  --out-csv reports/cankaya_next_7d_verified.csv \
  --out-report reports/cankaya_next_7d_verified.md
```

The verification compares overlapping pressure-level fields (`Z500`, `T850`,
850 hPa wind speed). It still does not verify surface station weather.
