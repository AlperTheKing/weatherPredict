# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260508T12Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |      bias |     corr |
|:-----------|----:|---------:|---------:|----------:|---------:|
| z500_m     |  28 | 13.6695  | 17.2981  |  7.89406  | 0.967698 |
| t850_c     |  28 |  1.43495 |  2.28516 | -0.634931 | 0.649998 |
| wind850_ms |  28 |  2.04415 |  2.39588 | -1.51035  | 0.466554 |
