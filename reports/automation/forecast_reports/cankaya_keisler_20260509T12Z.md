# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-09T12:00:00` UTC.
- Forecast range: `2026-05-09T12:00:00` to `2026-05-16T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `81.2s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-09T12:00:00 | 2026-05-09T12:00:00 |            0 |           0 |         40 |         33 |       5724.47 |      13.7654  |        1.48618 |       4.28651  |         5.84484 |           4.53684 |
| 2026-05-09T12:00:00 | 2026-05-10T12:00:00 |           24 |           1 |         40 |         33 |       5737.75 |      13.9684  |        3.49486 |       1.06234  |         6.79708 |           3.65275 |
| 2026-05-09T12:00:00 | 2026-05-11T12:00:00 |           48 |           2 |         40 |         33 |       5721.08 |      15.3979  |        3.11255 |       1.35915  |         7.22629 |           3.39636 |
| 2026-05-09T12:00:00 | 2026-05-12T12:00:00 |           72 |           3 |         40 |         33 |       5690.52 |      16.18    |        4.02024 |       1.49202  |         6.63614 |           4.28818 |
| 2026-05-09T12:00:00 | 2026-05-13T12:00:00 |           96 |           4 |         40 |         33 |       5632.45 |      15.623   |        5.7815  |       2.33158  |         5.4775  |           6.23394 |
| 2026-05-09T12:00:00 | 2026-05-14T12:00:00 |          120 |           5 |         40 |         33 |       5596.28 |      11.0579  |        4.22762 |      -1.14205  |         6.08367 |           4.37917 |
| 2026-05-09T12:00:00 | 2026-05-15T12:00:00 |          144 |           6 |         40 |         33 |       5596.62 |       9.20366 |        2.13281 |      -1.79711  |         5.88725 |           2.78899 |
| 2026-05-09T12:00:00 | 2026-05-16T12:00:00 |          168 |           7 |         40 |         33 |       5613.5  |      11.6105  |        1.51039 |       0.551508 |         5.11508 |           1.60793 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
