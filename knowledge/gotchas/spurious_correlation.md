# Spurious Correlation

**Slug:** `spurious_correlation`
**One-liner:** Two unrelated series share trend/seasonality and look correlated without a real link.

## What it is

Any two series with a monotone trend (or shared seasonality) will show a high correlation coefficient, regardless of whether they have any causal or even semantic relationship. Aggregated to low resolution, almost all macro time series correlate with almost all others.

## How to detect it

- Compute correlations on *changes* (first differences) or *residuals-after-detrending*, not levels, when the series trend.
- `stat_validate` warns when two inputs are both flagged non-stationary by an ADF test AND a correlation is being reported at raw levels.
- Eyeball for shared seasonality: if both series have a 12-month cycle, correlate the deseasonalized residuals.

## Mitigation

- Use `correlation` skill with `detrend="difference"` or `detrend="stl_residual"` on time series.
- Report the level correlation and the differenced correlation side-by-side; narrative should cite both.
- If the correlation survives differencing and is still "wow" — still check for a confounder.

## See also

- `non_stationarity`
- `confounding`
- Reference: Tyler Vigen, "Spurious Correlations" (illustrative catalog)
