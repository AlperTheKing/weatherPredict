# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-12T12:00:00` UTC.
- Forecast range: `2026-05-12T12:00:00` to `2026-05-19T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `15.6s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-12T12:00:00 | 2026-05-12T12:00:00 |            0 |           0 |         40 |         33 |       5686.76 |      16.0216  |        1.83737 |      3.1096    |         6.88222 |           3.61187 |
| 2026-05-12T12:00:00 | 2026-05-13T12:00:00 |           24 |           1 |         40 |         33 |       5651.09 |      15.2055  |        5.5546  |      0.772554  |         5.82046 |           5.60807 |
| 2026-05-12T12:00:00 | 2026-05-14T12:00:00 |           48 |           2 |         40 |         33 |       5588.38 |      11.7689  |        4.02849 |      0.821128  |         7.17481 |           4.11133 |
| 2026-05-12T12:00:00 | 2026-05-15T12:00:00 |           72 |           3 |         40 |         33 |       5597.05 |       8.95989 |        4.07828 |     -2.40147   |         4.71902 |           4.73281 |
| 2026-05-12T12:00:00 | 2026-05-16T12:00:00 |           96 |           4 |         40 |         33 |       5673.09 |      12.5099  |        3.20825 |      0.372872  |         4.79527 |           3.22984 |
| 2026-05-12T12:00:00 | 2026-05-17T12:00:00 |          120 |           5 |         40 |         33 |       5648.57 |      14.2475  |        5.17129 |      3.0429    |         7.20866 |           6.00013 |
| 2026-05-12T12:00:00 | 2026-05-18T12:00:00 |          144 |           6 |         40 |         33 |       5585.57 |      10.3525  |        5.09844 |     -0.844107  |         5.60127 |           5.16784 |
| 2026-05-12T12:00:00 | 2026-05-19T12:00:00 |          168 |           7 |         40 |         33 |       5585.39 |      10.453   |        3.6789  |      0.0120254 |         5.41823 |           3.67892 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
