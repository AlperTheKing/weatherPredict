# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260507T00Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |      bias |     corr |
|:-----------|----:|---------:|---------:|----------:|---------:|
| z500_m     |  28 | 26.4688  | 42.6498  | 24.0034   | 0.288729 |
| t850_c     |  28 |  1.15177 |  1.57221 |  0.291305 | 0.838355 |
| wind850_ms |  28 |  1.90107 |  2.47229 | -1.57799  | 0.221635 |
