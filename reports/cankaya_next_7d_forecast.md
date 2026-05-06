# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-06T00:00:00` UTC.
- Forecast range: `2026-05-06T00:00:00` to `2026-05-13T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `35.6s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-06T00:00:00 | 2026-05-06T00:00:00 |            0 |           0 |         40 |         33 |       5583.23 |       4.17614 |      -0.557083 |     -0.0128021 |         5.48556 |          0.55723  |
| 2026-05-06T00:00:00 | 2026-05-07T00:00:00 |           24 |           1 |         40 |         33 |       5648.28 |       6.29498 |       0.875984 |      0.364356  |         4.83949 |          0.948738 |
| 2026-05-06T00:00:00 | 2026-05-08T00:00:00 |           48 |           2 |         40 |         33 |       5706.51 |       9.76682 |       1.91106  |     -0.240464  |         4.49198 |          1.92613  |
| 2026-05-06T00:00:00 | 2026-05-09T00:00:00 |           72 |           3 |         40 |         33 |       5727.53 |      11.7079  |       0.547456 |      0.443531  |         4.79017 |          0.704576 |
| 2026-05-06T00:00:00 | 2026-05-10T00:00:00 |           96 |           4 |         40 |         33 |       5708.24 |      10.5536  |      -0.14191  |      0.542215  |         6.46183 |          0.560478 |
| 2026-05-06T00:00:00 | 2026-05-11T00:00:00 |          120 |           5 |         40 |         33 |       5740.46 |      11.6624  |       0.501348 |     -0.199826  |         7.10735 |          0.539704 |
| 2026-05-06T00:00:00 | 2026-05-12T00:00:00 |          144 |           6 |         40 |         33 |       5756.66 |      12.8333  |       1.5372   |     -1.80791   |         6.73982 |          2.37308  |
| 2026-05-06T00:00:00 | 2026-05-13T00:00:00 |          168 |           7 |         40 |         33 |       5759.56 |      14.3771  |       1.22703  |     -2.0956    |         6.00919 |          2.4284   |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
