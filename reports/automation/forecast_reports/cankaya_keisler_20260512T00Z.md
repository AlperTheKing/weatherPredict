# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-12T00:00:00` UTC.
- Forecast range: `2026-05-12T00:00:00` to `2026-05-19T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `35.5s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-12T00:00:00 | 2026-05-12T00:00:00 |            0 |           0 |         40 |         33 |       5698.09 |      13.1066  |        3.3623  |       3.0739   |         6.49302 |           4.55565 |
| 2026-05-12T00:00:00 | 2026-05-13T00:00:00 |           24 |           1 |         40 |         33 |       5625.37 |      12.2933  |        5.9863  |       1.73171  |         6.78961 |           6.23174 |
| 2026-05-12T00:00:00 | 2026-05-14T00:00:00 |           48 |           2 |         40 |         33 |       5631.76 |      12.8201  |        2.08978 |       2.23444  |         6.23879 |           3.05939 |
| 2026-05-12T00:00:00 | 2026-05-15T00:00:00 |           72 |           3 |         40 |         33 |       5565.49 |       6.00407 |        2.34834 |      -2.7715   |         5.7469  |           3.63262 |
| 2026-05-12T00:00:00 | 2026-05-16T00:00:00 |           96 |           4 |         40 |         33 |       5624.48 |       7.4491  |        3.07318 |      -1.10958  |         4.5755  |           3.26735 |
| 2026-05-12T00:00:00 | 2026-05-17T00:00:00 |          120 |           5 |         40 |         33 |       5655.86 |      12.1632  |        2.69937 |       3.65181  |         5.45161 |           4.54118 |
| 2026-05-12T00:00:00 | 2026-05-18T00:00:00 |          144 |           6 |         40 |         33 |       5589.45 |       8.86171 |        2.81077 |      -0.686747 |         6.35129 |           2.89345 |
| 2026-05-12T00:00:00 | 2026-05-19T00:00:00 |          168 |           7 |         40 |         33 |       5565.65 |       7.03731 |        3.93872 |      -1.3818   |         5.54524 |           4.17408 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
