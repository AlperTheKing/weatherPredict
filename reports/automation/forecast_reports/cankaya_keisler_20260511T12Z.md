# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-11T12:00:00` UTC.
- Forecast range: `2026-05-11T12:00:00` to `2026-05-18T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `38.3s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-11T12:00:00 | 2026-05-11T12:00:00 |            0 |           0 |         40 |         33 |       5722.75 |      13.6671  |        4.30139 |      0.932846  |         7.66018 |           4.40138 |
| 2026-05-11T12:00:00 | 2026-05-12T12:00:00 |           24 |           1 |         40 |         33 |       5692.02 |      16.0581  |        4.05058 |      1.98184   |         7.11885 |           4.50942 |
| 2026-05-11T12:00:00 | 2026-05-13T12:00:00 |           48 |           2 |         40 |         33 |       5644.89 |      14.5888  |        6.1685  |      0.0301876 |         5.69697 |           6.16858 |
| 2026-05-11T12:00:00 | 2026-05-14T12:00:00 |           72 |           3 |         40 |         33 |       5586.97 |      10.5564  |        4.17716 |     -0.721312  |         6.92263 |           4.23898 |
| 2026-05-11T12:00:00 | 2026-05-15T12:00:00 |           96 |           4 |         40 |         33 |       5600.19 |       9.22569 |        3.43473 |     -1.65535   |         4.36125 |           3.81282 |
| 2026-05-11T12:00:00 | 2026-05-16T12:00:00 |          120 |           5 |         40 |         33 |       5650.87 |      12.5893  |        3.44525 |      0.437349  |         4.75989 |           3.4729  |
| 2026-05-11T12:00:00 | 2026-05-17T12:00:00 |          144 |           6 |         40 |         33 |       5623.58 |      12.3742  |        5.90491 |      1.59439   |         6.25595 |           6.11638 |
| 2026-05-11T12:00:00 | 2026-05-18T12:00:00 |          168 |           7 |         40 |         33 |       5597.43 |       9.83937 |        6.51716 |     -1.52391   |         5.17362 |           6.69296 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
