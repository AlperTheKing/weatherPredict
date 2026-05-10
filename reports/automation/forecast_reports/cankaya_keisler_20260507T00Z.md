# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-07T00:00:00` UTC.
- Forecast range: `2026-05-07T00:00:00` to `2026-05-14T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `40.2s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-07T00:00:00 | 2026-05-07T00:00:00 |            0 |           0 |         40 |         33 |       5643.1  |       6.574   |       2.20061  |       0.717651 |         4.76077 |           2.31467 |
| 2026-05-07T00:00:00 | 2026-05-08T00:00:00 |           24 |           1 |         40 |         33 |       5711.98 |       9.88878 |       2.91703  |      -0.540389 |         4.45456 |           2.96666 |
| 2026-05-07T00:00:00 | 2026-05-09T00:00:00 |           48 |           2 |         40 |         33 |       5737.82 |      11.3667  |       0.872216 |       0.735773 |         5.5049  |           1.14111 |
| 2026-05-07T00:00:00 | 2026-05-10T00:00:00 |           72 |           3 |         40 |         33 |       5715.02 |      10.949   |       1.09456  |       0.981724 |         6.87649 |           1.47032 |
| 2026-05-07T00:00:00 | 2026-05-11T00:00:00 |           96 |           4 |         40 |         33 |       5727.09 |      11.5132  |       1.40092  |      -0.374239 |         7.05849 |           1.45004 |
| 2026-05-07T00:00:00 | 2026-05-12T00:00:00 |          120 |           5 |         40 |         33 |       5725.32 |      12.7516  |       2.18672  |      -0.942292 |         6.72561 |           2.3811  |
| 2026-05-07T00:00:00 | 2026-05-13T00:00:00 |          144 |           6 |         40 |         33 |       5732.36 |      14.6174  |       2.64272  |      -0.306452 |         6.06884 |           2.66043 |
| 2026-05-07T00:00:00 | 2026-05-14T00:00:00 |          168 |           7 |         40 |         33 |       5693.86 |      16.5536  |       2.44123  |       2.77477  |         5.43714 |           3.6958  |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
