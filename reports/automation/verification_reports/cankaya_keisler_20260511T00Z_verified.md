# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260511T00Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |       bias |     corr |
|:-----------|----:|---------:|---------:|-----------:|---------:|
| z500_m     |  28 | 20.8559  | 32.5247  | -15.9      | 0.846435 |
| t850_c     |  28 |  1.55251 |  1.94616 |  -1.12055  | 0.853992 |
| wind850_ms |  28 |  1.85281 |  2.20576 |  -0.841168 | 0.516384 |
