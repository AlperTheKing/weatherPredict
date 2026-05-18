# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260509T12Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |      bias |     corr |
|:-----------|----:|---------:|---------:|----------:|---------:|
| z500_m     |  28 | 13.5634  | 17.9924  | -0.685151 | 0.951957 |
| t850_c     |  28 |  1.04033 |  1.48603 | -0.255164 | 0.866745 |
| wind850_ms |  28 |  1.92046 |  2.15627 | -1.23073  | 0.527947 |
