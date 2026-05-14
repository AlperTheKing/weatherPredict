# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260506T12Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |       mae |     rmse |       bias |     corr |
|:-----------|----:|----------:|---------:|-----------:|---------:|
| z500_m     |  28 | 28.8625   | 47.3246  | 28.5675    | 0.345221 |
| t850_c     |  28 |  0.862748 |  1.18422 |  0.0883085 | 0.898481 |
| wind850_ms |  28 |  1.75139  |  2.2403  | -1.55751   | 0.473604 |
