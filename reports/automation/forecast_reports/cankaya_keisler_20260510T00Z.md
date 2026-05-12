# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-10T00:00:00` UTC.
- Forecast range: `2026-05-10T00:00:00` to `2026-05-17T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `107.2s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-10T00:00:00 | 2026-05-10T00:00:00 |            0 |           0 |         40 |         33 |       5712.45 |       9.74356 |       6.24022  |       0.785156 |         7.89645 |           6.28942 |
| 2026-05-10T00:00:00 | 2026-05-11T00:00:00 |           24 |           1 |         40 |         33 |       5723.7  |      11.9686  |       1.94859  |       0.356965 |         7.14042 |           1.98102 |
| 2026-05-10T00:00:00 | 2026-05-12T00:00:00 |           48 |           2 |         40 |         33 |       5691.44 |      12.7655  |       3.03111  |       1.14604  |         7.24301 |           3.24053 |
| 2026-05-10T00:00:00 | 2026-05-13T00:00:00 |           72 |           3 |         40 |         33 |       5644.4  |      13.6274  |       4.80693  |       2.04728  |         6.56986 |           5.22475 |
| 2026-05-10T00:00:00 | 2026-05-14T00:00:00 |           96 |           4 |         40 |         33 |       5606.9  |      11.3212  |       5.16394  |       1.31959  |         6.0767  |           5.32988 |
| 2026-05-10T00:00:00 | 2026-05-15T00:00:00 |          120 |           5 |         40 |         33 |       5581.53 |       6.89073 |       2.1942   |      -2.87153  |         5.97528 |           3.61389 |
| 2026-05-10T00:00:00 | 2026-05-16T00:00:00 |          144 |           6 |         40 |         33 |       5606.06 |       7.70172 |       1.70429  |      -0.7007   |         5.49331 |           1.84271 |
| 2026-05-10T00:00:00 | 2026-05-17T00:00:00 |          168 |           7 |         40 |         33 |       5578.72 |       8.94705 |       0.767899 |       2.66645  |         6.42181 |           2.77482 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
