# Çankaya 7-Day Forecast Verification

- Forecast CSV: `/Users/alper/Projects/weatherPredict/reports/automation/forecasts/cankaya_keisler_20260509T00Z.csv`.
- Rows with reference values: `28` / `28`.
- Reference source: Open-Meteo historical-forecast ECMWF IFS 0.25 pressure-level fields.

## Accuracy

| field      |   n |      mae |     rmse |      bias |     corr |
|:-----------|----:|---------:|---------:|----------:|---------:|
| z500_m     |  28 | 13.0039  | 17.1287  |  5.60947  | 0.963627 |
| t850_c     |  28 |  1.42278 |  2.17078 | -0.752584 | 0.760298 |
| wind850_ms |  28 |  2.24193 |  2.58796 | -1.70029  | 0.324455 |
