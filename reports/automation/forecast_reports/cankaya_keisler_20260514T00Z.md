# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-14T00:00:00` UTC.
- Forecast range: `2026-05-14T00:00:00` to `2026-05-21T00:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `96.7s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-14T00:00:00 | 2026-05-14T00:00:00 |            0 |           0 |         40 |         33 |       5624.24 |      13.2658  |      -0.960373 |       1.77007  |         6.21846 |           2.01381 |
| 2026-05-14T00:00:00 | 2026-05-15T00:00:00 |           24 |           1 |         40 |         33 |       5539.82 |       5.84917 |       3.6694   |      -2.85347  |         5.57206 |           4.64832 |
| 2026-05-14T00:00:00 | 2026-05-16T00:00:00 |           48 |           2 |         40 |         33 |       5615.36 |       7.63912 |       2.59705  |      -1.09369  |         4.49864 |           2.81795 |
| 2026-05-14T00:00:00 | 2026-05-17T00:00:00 |           72 |           3 |         40 |         33 |       5616.63 |      10.696   |       2.67788  |       3.20703  |         5.68438 |           4.17805 |
| 2026-05-14T00:00:00 | 2026-05-18T00:00:00 |           96 |           4 |         40 |         33 |       5569.97 |       6.25909 |       6.60916  |      -2.47128  |         5.63354 |           7.05608 |
| 2026-05-14T00:00:00 | 2026-05-19T00:00:00 |          120 |           5 |         40 |         33 |       5651.32 |       7.11264 |       1.63379  |      -2.84143  |         5.4436  |           3.27765 |
| 2026-05-14T00:00:00 | 2026-05-20T00:00:00 |          144 |           6 |         40 |         33 |       5651.24 |      11.0194  |      -1.31249  |       0.741122 |         5.28814 |           1.50728 |
| 2026-05-14T00:00:00 | 2026-05-21T00:00:00 |          168 |           7 |         40 |         33 |       5580.78 |       8.01579 |       0.743677 |      -1.72301  |         6.9663  |           1.87665 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
