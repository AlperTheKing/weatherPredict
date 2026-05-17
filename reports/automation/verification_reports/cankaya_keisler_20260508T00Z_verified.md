# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260508T00Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |     bias |     corr |
|:-----------|----:|---------:|---------:|---------:|---------:|
| z500_m     |  28 | 10.7083  | 16.3341  | -2.25278 | 0.958732 |
| t850_c     |  28 |  1.80396 |  2.81073 | -1.47159 | 0.397502 |
| wind850_ms |  28 |  2.18666 |  2.52063 | -1.60813 | 0.42552  |
