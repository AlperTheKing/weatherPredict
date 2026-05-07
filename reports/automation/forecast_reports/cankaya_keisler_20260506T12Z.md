# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-06T12:00:00` UTC.
- Forecast range: `2026-05-06T12:00:00` to `2026-05-13T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `36.6s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-06T12:00:00 | 2026-05-06T12:00:00 |            0 |           0 |         40 |         33 |       5625.7  |       7.62014 |        2.55342 |       2.07863  |         4.70736 |           3.29252 |
| 2026-05-06T12:00:00 | 2026-05-07T12:00:00 |           24 |           1 |         40 |         33 |       5697.7  |      10.4524  |        2.72815 |       0.416765 |         4.63825 |           2.7598  |
| 2026-05-06T12:00:00 | 2026-05-08T12:00:00 |           48 |           2 |         40 |         33 |       5746.84 |      13.2711  |        2.51042 |      -0.468219 |         4.70122 |           2.55371 |
| 2026-05-06T12:00:00 | 2026-05-09T12:00:00 |           72 |           3 |         40 |         33 |       5732.35 |      12.1917  |        1.45736 |       1.18903  |         6.63432 |           1.88088 |
| 2026-05-06T12:00:00 | 2026-05-10T12:00:00 |           96 |           4 |         40 |         33 |       5732.67 |      13.6569  |        2.66071 |       0.382792 |         6.95264 |           2.68811 |
| 2026-05-06T12:00:00 | 2026-05-11T12:00:00 |          120 |           5 |         40 |         33 |       5753.57 |      15.1591  |        2.2499  |      -0.8962   |         6.50694 |           2.42182 |
| 2026-05-06T12:00:00 | 2026-05-12T12:00:00 |          144 |           6 |         40 |         33 |       5764.53 |      16.0698  |        2.00973 |      -2.20254  |         5.57841 |           2.98165 |
| 2026-05-06T12:00:00 | 2026-05-13T12:00:00 |          168 |           7 |         40 |         33 |       5733.45 |      18.2751  |        4.22429 |       0.043183 |         5.30302 |           4.22451 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
