# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-09T00:00:00` UTC.
- Forecast range: `2026-05-09T00:00:00` to `2026-05-16T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `163.0s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-09T00:00:00 | 2026-05-09T00:00:00 |            0 |           0 |         40 |         33 |       5731.41 |      12.7282  |      -2.533    |       1.19617  |         5.43981 |           2.80124 |
| 2026-05-09T00:00:00 | 2026-05-10T00:00:00 |           24 |           1 |         40 |         33 |       5714.8  |      10.6476  |       1.88839  |       0.975132 |         7.00293 |           2.1253  |
| 2026-05-09T00:00:00 | 2026-05-11T00:00:00 |           48 |           2 |         40 |         33 |       5735.09 |      12.8118  |       0.995203 |       0.599672 |         6.80033 |           1.16191 |
| 2026-05-09T00:00:00 | 2026-05-12T00:00:00 |           72 |           3 |         40 |         33 |       5701.96 |      13.3852  |       2.81378  |       1.2331   |         7.15021 |           3.07211 |
| 2026-05-09T00:00:00 | 2026-05-13T00:00:00 |           96 |           4 |         40 |         33 |       5661.31 |      13.6426  |       4.26538  |       1.24878  |         6.70387 |           4.44443 |
| 2026-05-09T00:00:00 | 2026-05-14T00:00:00 |          120 |           5 |         40 |         33 |       5602.93 |       8.49845 |       2.45229  |      -1.87938  |         6.71977 |           3.08963 |
| 2026-05-09T00:00:00 | 2026-05-15T00:00:00 |          144 |           6 |         40 |         33 |       5578.6  |       6.44092 |       0.535784 |      -2.2274   |         6.15311 |           2.29093 |
| 2026-05-09T00:00:00 | 2026-05-16T00:00:00 |          168 |           7 |         40 |         33 |       5600.97 |       5.6873  |       2.11465  |      -2.20336  |         4.99642 |           3.05394 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
