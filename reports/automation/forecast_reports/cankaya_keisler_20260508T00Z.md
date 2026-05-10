# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-08T00:00:00` UTC.
- Forecast range: `2026-05-08T00:00:00` to `2026-05-15T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `40.8s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-08T00:00:00 | 2026-05-08T00:00:00 |            0 |           0 |         40 |         33 |       5702    |      10.2705  |       2.97441  |     -0.119888  |         5.16513 |           2.97683 |
| 2026-05-08T00:00:00 | 2026-05-09T00:00:00 |           24 |           1 |         40 |         33 |       5732.02 |      11.5142  |       0.790098 |      0.69517   |         5.40618 |           1.05239 |
| 2026-05-08T00:00:00 | 2026-05-10T00:00:00 |           48 |           2 |         40 |         33 |       5713.5  |      10.5964  |       2.10755  |      1.0413    |         7.006   |           2.35076 |
| 2026-05-08T00:00:00 | 2026-05-11T00:00:00 |           72 |           3 |         40 |         33 |       5728.42 |      11.9533  |       1.13058  |     -0.304643  |         6.91905 |           1.17091 |
| 2026-05-08T00:00:00 | 2026-05-12T00:00:00 |           96 |           4 |         40 |         33 |       5688.08 |      12.3286  |       2.85606  |      0.574292  |         7.06482 |           2.91322 |
| 2026-05-08T00:00:00 | 2026-05-13T00:00:00 |          120 |           5 |         40 |         33 |       5636.2  |      11.0379  |       4.61163  |      0.0294715 |         6.97889 |           4.61173 |
| 2026-05-08T00:00:00 | 2026-05-14T00:00:00 |          144 |           6 |         40 |         33 |       5596.86 |       6.43113 |       1.36307  |     -2.68288   |         6.16061 |           3.00929 |
| 2026-05-08T00:00:00 | 2026-05-15T00:00:00 |          168 |           7 |         40 |         33 |       5577.45 |       8.33359 |       2.64896  |      0.163496  |         5.09602 |           2.654   |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
