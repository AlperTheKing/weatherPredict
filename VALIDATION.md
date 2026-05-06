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
| CPU 10-day timing | `uv run forecast.py --init 2020-01-01T00 --steps 40 --timing --out /tmp/keisler_10d_cpu.nc` | Passed; total 153.5s, output 795M |
| Apple Metal probe | `ENABLE_PJRT_COMPATIBILITY=1 uv run python -c "import jax; print(jax.devices()); print(jax.numpy.arange(10))"` | Failed; device visible but simple JAX op fails |

## Build Notes

The first `uv sync --frozen --extra scripts --extra opendata` attempt let `uv`
choose CPython 3.14.3. That made `h3==3.7.7` build from source and fail in CMake
because the bundled H3 CMakeLists requests compatibility removed by the installed
CMake. Adding `.python-version` with `3.11` and running with `--python 3.11`
resolved this by using compatible wheels.

## ERA5 RMSE

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

## Notes

- Large forecast outputs are written under `/tmp` and are not committed.
- Apple `jax-metal` is experimental. CPU validation is the baseline if Metal
  backend support fails or lacks required JAX operations.
