# Çankaya 7-Day Keisler Forecast

This is a pressure-level point forecast, not a surface station forecast.

## Scope

- Requested location: latitude `39.9179`, longitude `32.8627`.
- Nearest model grid point: latitude `40.0`, longitude `33.0`.
- Initialization source: ECMWF Open Data 0h analysis converted to the Keisler input contract.
- Initialization time: `2026-05-08T12:00:00` UTC.
- Forecast range: `2026-05-08T12:00:00` to `2026-05-15T12:00:00`.
- Cadence: 6 hours in the CSV; 24-hour rows shown below.
- Runtime: `34.4s`.

## Daily Rows

| init_time           | target_time         |   lead_hours |   lead_days |   grid_lat |   grid_lon |   pred_z500_m |   pred_t850_c |   pred_u850_ms |   pred_v850_ms |   pred_q850_gkg |   pred_wind850_ms |
|:--------------------|:--------------------|-------------:|------------:|-----------:|-----------:|--------------:|--------------:|---------------:|---------------:|----------------:|------------------:|
| 2026-05-08T12:00:00 | 2026-05-08T12:00:00 |            0 |           0 |         40 |         33 |       5742.7  |      13.7047  |        2.9227  |       0.641541 |         4.21912 |           2.99228 |
| 2026-05-08T12:00:00 | 2026-05-09T12:00:00 |           24 |           1 |         40 |         33 |       5734.98 |      12.7523  |        1.88809 |       1.77718  |         6.5195  |           2.59293 |
| 2026-05-08T12:00:00 | 2026-05-10T12:00:00 |           48 |           2 |         40 |         33 |       5741.27 |      14.5617  |        3.66933 |       0.772987 |         6.44915 |           3.74986 |
| 2026-05-08T12:00:00 | 2026-05-11T12:00:00 |           72 |           3 |         40 |         33 |       5732    |      16.192   |        2.80766 |       1.13792  |         6.90367 |           3.02949 |
| 2026-05-08T12:00:00 | 2026-05-12T12:00:00 |           96 |           4 |         40 |         33 |       5703.92 |      16.5692  |        3.88012 |       1.31576  |         6.40619 |           4.09714 |
| 2026-05-08T12:00:00 | 2026-05-13T12:00:00 |          120 |           5 |         40 |         33 |       5630.45 |      12.7139  |        4.94867 |      -1.29571  |         6.51197 |           5.11549 |
| 2026-05-08T12:00:00 | 2026-05-14T12:00:00 |          144 |           6 |         40 |         33 |       5608.7  |      10.3136  |        2.23322 |      -1.22919  |         5.77787 |           2.54915 |
| 2026-05-08T12:00:00 | 2026-05-15T12:00:00 |          168 |           7 |         40 |         33 |       5585.36 |       8.71317 |        3.5107  |      -1.91677  |         5.59959 |           3.99988 |

## Verification

Run `scripts/06_verify_point_forecast.py` after the target dates have observed or
analysis reference values available.
