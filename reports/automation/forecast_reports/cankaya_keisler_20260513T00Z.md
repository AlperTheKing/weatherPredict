# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-13T00:00:00` UTC.
- Forecast range: `2026-05-13T00:00:00` to `2026-05-20T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `52.7s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-13T00:00:00 | 2026-05-13T00:00:00 |            0 |           0 |         40 |         33 |       5624.58 |      11.1971  |       1.60062  |      -1.6602   |         6.99661 |           2.30613 |
| 2026-05-13T00:00:00 | 2026-05-14T00:00:00 |           24 |           1 |         40 |         33 |       5630.71 |      12.4628  |       0.677363 |       2.20303  |         6.52015 |           2.30481 |
| 2026-05-13T00:00:00 | 2026-05-15T00:00:00 |           48 |           2 |         40 |         33 |       5559.02 |       5.6393  |       4.84348  |      -2.80121  |         5.57687 |           5.59519 |
| 2026-05-13T00:00:00 | 2026-05-16T00:00:00 |           72 |           3 |         40 |         33 |       5634.3  |       7.56548 |       2.92384  |      -0.593493 |         4.80161 |           2.98346 |
| 2026-05-13T00:00:00 | 2026-05-17T00:00:00 |           96 |           4 |         40 |         33 |       5656.14 |      11.2208  |       2.21763  |       3.8865   |         6.01676 |           4.47468 |
| 2026-05-13T00:00:00 | 2026-05-18T00:00:00 |          120 |           5 |         40 |         33 |       5577.67 |       8.13893 |       5.85707  |      -1.40611  |         5.75457 |           6.02349 |
| 2026-05-13T00:00:00 | 2026-05-19T00:00:00 |          144 |           6 |         40 |         33 |       5597.86 |       5.92702 |       6.04269  |      -4.05649  |         5.86297 |           7.27799 |
| 2026-05-13T00:00:00 | 2026-05-20T00:00:00 |          168 |           7 |         40 |         33 |       5612.68 |       8.34789 |       1.54509  |      -1.1426   |         6.0811  |           1.92168 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
