# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-13T12:00:00` UTC.
- Forecast range: `2026-05-13T12:00:00` to `2026-05-20T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `32.8s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-13T12:00:00 | 2026-05-13T12:00:00 |            0 |           0 |         40 |         33 |       5653.52 |      15.6196  |       9.04382  |      3.85577   |         5.78311 |           9.83147 |
| 2026-05-13T12:00:00 | 2026-05-14T12:00:00 |           24 |           1 |         40 |         33 |       5586.66 |      10.775   |       3.83087  |     -0.0900565 |         7.42634 |           3.83193 |
| 2026-05-13T12:00:00 | 2026-05-15T12:00:00 |           48 |           2 |         40 |         33 |       5599.37 |       8.91364 |       3.23549  |     -1.91597   |         4.47731 |           3.76023 |
| 2026-05-13T12:00:00 | 2026-05-16T12:00:00 |           72 |           3 |         40 |         33 |       5662.25 |      12.7055  |       2.89856  |      0.313982  |         4.39881 |           2.91552 |
| 2026-05-13T12:00:00 | 2026-05-17T12:00:00 |           96 |           4 |         40 |         33 |       5628.02 |      12.386   |       6.01637  |      1.28451   |         6.70866 |           6.15197 |
| 2026-05-13T12:00:00 | 2026-05-18T12:00:00 |          120 |           5 |         40 |         33 |       5618.62 |       8.34432 |       7.37426  |     -3.7191    |         5.58146 |           8.25902 |
| 2026-05-13T12:00:00 | 2026-05-19T12:00:00 |          144 |           6 |         40 |         33 |       5652.5  |      11.2713  |       3.70041  |     -1.98563   |         5.1082  |           4.19949 |
| 2026-05-13T12:00:00 | 2026-05-20T12:00:00 |          168 |           7 |         40 |         33 |       5619.84 |      11.4494  |       0.519286 |     -0.938413  |         5.80664 |           1.07251 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
