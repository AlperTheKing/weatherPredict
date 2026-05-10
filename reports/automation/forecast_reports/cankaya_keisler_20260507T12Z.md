# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-07T12:00:00` UTC.
- Forecast range: `2026-05-07T12:00:00` to `2026-05-14T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `54.6s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-07T12:00:00 | 2026-05-07T12:00:00 |            0 |           0 |         40 |         33 |       5699.23 |       10.9473 |        3.48004 |       0.73941  |         4.44796 |           3.55773 |
| 2026-05-07T12:00:00 | 2026-05-08T12:00:00 |           24 |           1 |         40 |         33 |       5746.34 |       13.2043 |        2.9138  |      -0.175775 |         5.00579 |           2.91909 |
| 2026-05-07T12:00:00 | 2026-05-09T12:00:00 |           48 |           2 |         40 |         33 |       5727.53 |       12.075  |        1.81186 |       1.30133  |         6.91784 |           2.23076 |
| 2026-05-07T12:00:00 | 2026-05-10T12:00:00 |           72 |           3 |         40 |         33 |       5732.34 |       13.7551 |        3.62251 |       0.329371 |         6.87978 |           3.63745 |
| 2026-05-07T12:00:00 | 2026-05-11T12:00:00 |           96 |           4 |         40 |         33 |       5721.45 |       14.7545 |        2.0714  |       0.374373 |         7.02094 |           2.10496 |
| 2026-05-07T12:00:00 | 2026-05-12T12:00:00 |          120 |           5 |         40 |         33 |       5692.43 |       15.7741 |        4.42777 |       1.07454  |         6.23478 |           4.55629 |
| 2026-05-07T12:00:00 | 2026-05-13T12:00:00 |          144 |           6 |         40 |         33 |       5636    |       14.4888 |        4.44059 |       1.5653   |         5.97204 |           4.7084  |
| 2026-05-07T12:00:00 | 2026-05-14T12:00:00 |          168 |           7 |         40 |         33 |       5594.18 |       10.8361 |        4.58838 |       0.499671 |         5.80355 |           4.61551 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
