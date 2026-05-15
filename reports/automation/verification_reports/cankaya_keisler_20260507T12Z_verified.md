# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260507T12Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |     mae |     rmse |       bias |     corr |
|:-----------|----:|--------:|---------:|-----------:|---------:|
| z500_m     |  28 | 9.37746 | 14.0996  |  0.0375208 | 0.955288 |
| t850_c     |  28 | 1.20896 |  1.81899 | -0.904451  | 0.587388 |
| wind850_ms |  28 | 1.8803  |  2.23448 | -1.18355   | 0.401161 |
