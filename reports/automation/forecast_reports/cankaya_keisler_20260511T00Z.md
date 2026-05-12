# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-11T00:00:00` UTC.
- Forecast range: `2026-05-11T00:00:00` to `2026-05-18T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `169.5s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-11T00:00:00 | 2026-05-11T00:00:00 |            0 |           0 |         40 |         33 |       5728.38 |      13.4079  |        1.27216 |       1.9953   |         6.92012 |           2.36635 |
| 2026-05-11T00:00:00 | 2026-05-12T00:00:00 |           24 |           1 |         40 |         33 |       5690.89 |      12.7639  |        3.10349 |       0.493012 |         7.0576  |           3.14241 |
| 2026-05-11T00:00:00 | 2026-05-13T00:00:00 |           48 |           2 |         40 |         33 |       5627.41 |      12.8329  |        4.93735 |       1.79011  |         6.60641 |           5.25185 |
| 2026-05-11T00:00:00 | 2026-05-14T00:00:00 |           72 |           3 |         40 |         33 |       5621.08 |      10.7368  |        2.82516 |       0.472729 |         6.52507 |           2.86444 |
| 2026-05-11T00:00:00 | 2026-05-15T00:00:00 |           96 |           4 |         40 |         33 |       5555.1  |       6.63714 |        3.5013  |      -2.32922  |         5.95919 |           4.20528 |
| 2026-05-11T00:00:00 | 2026-05-16T00:00:00 |          120 |           5 |         40 |         33 |       5594.92 |       8.219   |        3.14607 |       0.607035 |         5.16111 |           3.2041  |
| 2026-05-11T00:00:00 | 2026-05-17T00:00:00 |          144 |           6 |         40 |         33 |       5560.07 |       8.10844 |        3.89721 |       2.98321  |         6.78033 |           4.90793 |
| 2026-05-11T00:00:00 | 2026-05-18T00:00:00 |          168 |           7 |         40 |         33 |       5594.08 |       5.35319 |        4.82308 |      -4.41744  |         5.79919 |           6.54032 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
