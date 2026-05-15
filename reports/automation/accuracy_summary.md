# Cankaya Automated Forecast Accuracy

- Last update: `2026-05-15T22:00:05.458580+03:00`.
- Forecast files: `16`.
- Verified forecast files: `3`.
- Scored rows: `84`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.
- Percentage column: range-normalized diagnostic only; MAE, RMSE, bias, corr, and persistence skill are the primary metrics.

## Overall Metrics

| field      |   n |      mae |     rmse |      bias |     corr |   actual_range |   range_accuracy_pct |   persistence_rmse |   skill_vs_persistence_pct |
|:-----------|----:|---------:|---------:|----------:|---------:|---------------:|---------------------:|-------------------:|---------------------------:|
| z500_m     |  84 | 21.5696  | 37.6715  | 17.5361   | 0.621017 |      162       |              86.6854 |           66.8398  |                    43.6391 |
| t850_c     |  84 |  1.07449 |  1.54736 | -0.174946 | 0.790722 |       10.3     |              89.568  |            4.93231 |                    68.6281 |
| wind850_ms |  84 |  1.84425 |  2.31834 | -1.43968  | 0.361405 |        8.22222 |              77.5699 |            2.15916 |                    -7.372  |

## By Forecast Run

| forecast_id   | init_time           |   rows_scored | target_start        | target_end          |   z500_m_mae |   z500_m_rmse |   t850_c_mae |   t850_c_rmse |   wind850_ms_mae |   wind850_ms_rmse |
|:--------------|:--------------------|--------------:|:--------------------|:--------------------|-------------:|--------------:|-------------:|--------------:|-----------------:|------------------:|
| 20260506T12Z  | 2026-05-06T12:00:00 |            28 | 2026-05-06T18:00:00 | 2026-05-13T12:00:00 |     28.8625  |       47.3246 |     0.862748 |       1.18422 |          1.75139 |           2.2403  |
| 20260507T00Z  | 2026-05-07T00:00:00 |            28 | 2026-05-07T06:00:00 | 2026-05-14T00:00:00 |     26.4688  |       42.6498 |     1.15177  |       1.57221 |          1.90107 |           2.47229 |
| 20260507T12Z  | 2026-05-07T12:00:00 |            28 | 2026-05-07T18:00:00 | 2026-05-14T12:00:00 |      9.37746 |       14.0996 |     1.20896  |       1.81899 |          1.8803  |           2.23448 |
