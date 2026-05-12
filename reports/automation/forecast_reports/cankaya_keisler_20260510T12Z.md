# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-10T12:00:00` UTC.
- Forecast range: `2026-05-10T12:00:00` to `2026-05-17T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `100.8s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-10T12:00:00 | 2026-05-10T12:00:00 |            0 |           0 |         40 |         33 |       5730.62 |      14.5453  |        6.85684 |       2.73306  |         6.00436 |           7.38146 |
| 2026-05-10T12:00:00 | 2026-05-11T12:00:00 |           24 |           1 |         40 |         33 |       5715.89 |      14.1462  |        2.91883 |       1.37821  |         7.57329 |           3.22785 |
| 2026-05-10T12:00:00 | 2026-05-12T12:00:00 |           48 |           2 |         40 |         33 |       5686.14 |      16.0535  |        4.39802 |       1.71046  |         6.91089 |           4.71892 |
| 2026-05-10T12:00:00 | 2026-05-13T12:00:00 |           72 |           3 |         40 |         33 |       5616.24 |      13.9316  |        6.22415 |       0.811834 |         5.9234  |           6.27687 |
| 2026-05-10T12:00:00 | 2026-05-14T12:00:00 |           96 |           4 |         40 |         33 |       5578.62 |      10.0976  |        4.59197 |      -1.46727  |         6.38867 |           4.82069 |
| 2026-05-10T12:00:00 | 2026-05-15T12:00:00 |          120 |           5 |         40 |         33 |       5610.3  |       8.97549 |        2.54622 |      -1.86283  |         5.10509 |           3.15489 |
| 2026-05-10T12:00:00 | 2026-05-16T12:00:00 |          144 |           6 |         40 |         33 |       5629.4  |      11.2904  |        1.84567 |       3.39778  |         5.82022 |           3.8667  |
| 2026-05-10T12:00:00 | 2026-05-17T12:00:00 |          168 |           7 |         40 |         33 |       5531.01 |       9.48259 |        4.80151 |      -0.336242 |         5.71508 |           4.81326 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
