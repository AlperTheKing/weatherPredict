# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260510T00Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |      bias |     corr |
|:-----------|----:|---------:|---------:|----------:|---------:|
| z500_m     |  28 | 14.6842  | 18.6325  | -3.41359  | 0.944933 |
| t850_c     |  28 |  1.13829 |  1.52048 | -0.641841 | 0.879062 |
| wind850_ms |  28 |  1.93394 |  2.33788 | -1.02416  | 0.421412 |
