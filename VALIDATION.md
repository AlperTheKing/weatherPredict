# Validation

Validation target:

- Repository: `weatherPredict`
- Upstream source: `rkeisler/keisler-2022`
- Imported commit: `d46ba88e49ed5f90f3247e3c39f3fdc1e6f6b78a`
- Local machine: macOS 26.4.1, Apple M4 Max, 40-core Apple GPU, 16 logical CPU
- Python: 3.11.15
- Package manager: `uv`

## Results

Status: CPU import/build validated. Apple Metal was probed but is not usable with
the installed JAX/jax-metal combination.

| Check | Command | Result |
| --- | --- | --- |
| Environment sync | `uv sync --python 3.11 --frozen --extra scripts --extra opendata` | Passed; 105 packages installed |
| JAX devices | `uv run python -c "import jax; print(jax.__version__, jax.devices())"` | Passed: `0.7.1 [CpuDevice(id=0)]` |
| Unit tests | `uv run pytest -m "not network"` | Passed: 27 passed, 2 deselected, 20.02s |
| 2-step regression | `uv run pytest tests/test_runner.py::test_two_steps_regression` | Passed: 1 passed, 852.31s |
| ERA5 RMSE, 12 steps | `uv run --extra scripts scripts/01_evaluation.py --init 2020-01-01T00 --steps 12 --fig /tmp/era5_eval_q850.png` | Stalled in remote ERA5 truth loading; interrupted after more than 1h40m |
| ERA5 RMSE, 1 step smoke | `uv run --extra scripts scripts/01_evaluation.py --init 2020-01-01T00 --steps 1 --fig /tmp/era5_eval_q850_1step.png` | Passed; figure written to `/tmp/era5_eval_q850_1step.png` |
| Sensitivity, 1 step smoke | `uv run --extra scripts scripts/02_sensitivity.py --init 2020-01-01T00 --steps 1 --fig /tmp/sensitivity_1step.png` | Passed; gradient 2.1s, figure written to `/tmp/sensitivity_1step.png` |
| CPU 10-day timing | `uv run forecast.py --init 2020-01-01T00 --steps 40 --timing --out /tmp/keisler_10d_cpu.nc` | Passed; total 153.5s, output 795M |
| Apple Metal probe | `ENABLE_PJRT_COMPATIBILITY=1 uv run python -c "import jax; print(jax.devices()); print(jax.numpy.arange(10))"` | Failed; device visible but simple JAX op fails |

## Build Notes

The first `uv sync --frozen --extra scripts --extra opendata` attempt let `uv`
choose CPython 3.14.3. That made `h3==3.7.7` build from source and fail in CMake
because the bundled H3 CMakeLists requests compatibility removed by the installed
CMake. Adding `.python-version` with `3.11` and running with `--python 3.11`
resolved this by using compatible wheels.

## ERA5 RMSE

Scope of the numeric accuracy values below:

- Data source: ERA5 reanalysis via Google ARCO.
- Initialization: `2020-01-01T00:00:00`.
- Verification period in the completed smoke run: +6h, `2020-01-01T06:00:00`.
- Geography: global 1-degree latitude/longitude grid, area weighted by
  `cos(latitude)`.
- Variables: `Z500` is geopotential at 500 hPa; `T850`, `U850`, and `Q850` are
  temperature, u-wind, and specific humidity at 850 hPa.

The full 12-step RMSE command did run the 12-step forecast successfully:

- Forecast completed in 6.3s on CPU.
- It then started loading 12 ERA5 truth slices from Google ARCO.
- The run reached `2020-01-03T12:00:00` truth loading and then stopped making
  progress; CPU usage was 0%, consistent with remote IO wait.
- `/tmp/era5_eval_q850.png` was not written.

The 1-step smoke RMSE completed:

| Lead (h) | Z500 | T850 | U850 | Q850 |
| ---: | ---: | ---: | ---: | ---: |
| 6 | 47.0181 | 0.7479 | 1.4233 | 0.000754 |

Additional correctness signal:

- `tests/test_runner.py::test_two_steps_regression` passed. This checks a
  specific final geopotential value and mean values across all forecast fields
  against upstream regression expectations.

## Sensitivity

The sensitivity script is present as `scripts/02_sensitivity.py`. It computes
JAX autodiff gradients of a selected forecast scalar with respect to the initial
conditions.

Completed smoke run:

- Initialization: `2020-01-01T00:00:00`.
- Lead: +6h (`--steps 1`).
- Target: `T850` at latitude `35.7`, longitude `254.1` in 0-360 convention
  (`105.9W`), node `19694`, channel `23`.
- Visualized input sensitivities: `d(T850) / d(Z500)` and `d(T850) / d(U500)`.
- Gradient computation time after prepare/JIT entry: 2.1s on CPU.
- Figure: `/tmp/sensitivity_1step.png`.

The upstream default example is a heavier +72h run (`--steps 12`) initialized at
`2026-01-03T00`; that was not run in this validation pass because the CPU
baseline already showed remote ERA5 loading as the dominant bottleneck.

## Runtime

10-day CPU forecast timing:

| Segment | Time |
| --- | ---: |
| Load initial conditions | 132.6s |
| JIT | 0.5s |
| 40 forecast steps | 19.9s |
| Forecast total | 20.4s |
| Write NetCDF | 0.3s |
| End-to-end total | 153.5s |

The 40-step output was `/tmp/keisler_10d_cpu.nc` and measured 795M.

Interpretation:

- The model compute path is fast on CPU: about 0.5s per 6-hour step in this run.
- The end-to-end CLI timing is dominated by remote initial-condition loading.
- The upstream README claim of roughly 2 minutes on an 8-vCPU CPU machine is
  directionally close here: this 16-logical-CPU Apple M4 Max CPU run measured
  153.5s end to end, including data load and output write.

## Apple Metal

Probe details:

- Installed package: `jax-metal==0.1.1`.
- `jax.devices()` reported `[METAL(id=0)]` and selected Apple M4 Max.
- `jax.numpy.arange(10)` failed before any forecast test with:
  `jaxlib._jax.XlaRuntimeError: UNKNOWN: ... unknown attribute code: 22 ... StableHLO_v1.10.8`.
- Because a basic JAX op failed, no 1-step or 40-step Metal forecast was run.
- `jax-metal` was uninstalled after the probe so the default environment returns
  to `0.7.1 [CpuDevice(id=0)]`.

## Çankaya Point Hindcast

Latest point-run artifact:

- Script: `scripts/04_point_hindcast.py`.
- Report: `reports/cankaya_2026_hindcast.md`.
- CSV: `reports/cankaya_2026_keisler_daily.csv`.
- Location request: Çankaya, Ankara, latitude `39.9179`, longitude `32.8627`.
- Model grid: `40.0N, 33.0E`.
- Forecast initialization: `2026-01-01T00:00:00`.
- Scored range: daily `2026-01-02T00:00:00` through `2026-05-06T00:00:00`.
- Forecast style: one autoregressive run sampled every 24 hours.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level
  fields at `40.0N, 32.75E`.

Accuracy over 125 daily targets:

| Field | MAE | RMSE | Bias | Corr |
| --- | ---: | ---: | ---: | ---: |
| z500_m | 70.4082 | 85.9772 | 3.0781 | 0.3152 |
| t850_c | 4.3244 | 5.2769 | -1.7011 | 0.3640 |
| wind850_ms | 3.7728 | 4.8285 | -2.6667 | 0.2611 |

## Forward 7-Day Forecast Setup

Latest generated forward-looking point forecast:

- Script: `scripts/05_point_weekly_forecast.py`.
- Later verification script: `scripts/06_verify_point_forecast.py`.
- Forecast report: `reports/cankaya_next_7d_forecast.md`.
- Forecast CSV: `reports/cankaya_next_7d_forecast.csv`.
- Location request: Çankaya, Ankara, latitude `39.9179`, longitude `32.8627`.
- Model grid: `40.0N, 33.0E`.
- Latest available ECMWF Open Data cycle at run time: `2026-05-06T00:00:00` UTC.
- Forecast range: `2026-05-06T00:00:00` through `2026-05-13T00:00:00`.
- Cadence: 6 hours in the CSV, daily rows in the report.
- Runtime: 35.6s.

Verification command for later:

```bash
uv run --extra scripts scripts/06_verify_point_forecast.py \
  --forecast-csv reports/cankaya_next_7d_forecast.csv \
  --out-csv reports/cankaya_next_7d_verified.csv \
  --out-report reports/cankaya_next_7d_verified.md
```

The verification compares pressure-level reference fields (`Z500`, `T850`, and
850 hPa wind speed). Surface observations are outside this model's output
contract.

## Notes

- Large forecast outputs are written under `/tmp` and are not committed.
- Apple `jax-metal` is experimental. CPU validation is the baseline if Metal
  backend support fails or lacks required JAX operations.
