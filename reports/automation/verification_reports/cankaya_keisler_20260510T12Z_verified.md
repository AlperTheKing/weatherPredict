# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260510T12Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |       bias |     corr |
|:-----------|----:|---------:|---------:|-----------:|---------:|
| z500_m     |  28 | 20.3413  | 30.2641  | -10.6986   | 0.869171 |
| t850_c     |  28 |  1.40165 |  1.86245 |  -0.926602 | 0.836517 |
| wind850_ms |  28 |  1.73313 |  2.01018 |  -0.859427 | 0.615195 |
