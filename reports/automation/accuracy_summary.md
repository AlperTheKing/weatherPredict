# Cankaya Automated Forecast Accuracy

- Last update: `2026-05-14T22:00:06.124920+03:00`.
- Forecast files: `16`.
- Verified forecast files: `1`.
- Scored rows: `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.
- Percentage column: range-normalized diagnostic only; MAE, RMSE, bias, corr, and persistence skill are the primary metrics.

## Overall Metrics

| field      |   n |       mae |     rmse |       bias |     corr |   actual_range |   range_accuracy_pct |   persistence_rmse |   skill_vs_persistence_pct |
|:-----------|----:|----------:|---------:|-----------:|---------:|---------------:|---------------------:|-------------------:|---------------------------:|
| z500_m     |  28 | 28.8625   | 47.3246  | 28.5675    | 0.345221 |      128       |              77.4511 |           82.5423  |                    42.6662 |
| t850_c     |  28 |  0.862748 |  1.18422 |  0.0883085 | 0.898481 |       10.3     |              91.6238 |            5.05727 |                    76.5837 |
| wind850_ms |  28 |  1.75139  |  2.2403  | -1.55751   | 0.473604 |        8.22222 |              78.6993 |            1.86892 |                   -19.8708 |

## By Forecast Run

| forecast_id   | init_time           |   rows_scored | target_start        | target_end          |   z500_m_mae |   z500_m_rmse |   t850_c_mae |   t850_c_rmse |   wind850_ms_mae |   wind850_ms_rmse |
|:--------------|:--------------------|--------------:|:--------------------|:--------------------|-------------:|--------------:|-------------:|--------------:|-----------------:|------------------:|
| 20260506T12Z  | 2026-05-06T12:00:00 |            28 | 2026-05-06T18:00:00 | 2026-05-13T12:00:00 |      28.8625 |       47.3246 |     0.862748 |       1.18422 |          1.75139 |            2.2403 |
