# Notebooks

## Current notebooks

- `../01_data_availability_and_exploration.ipynb`: data availability, integrity checks, trading-session alignment, and exploratory analysis.
- `02_feature_engineering.ipynb`: scheduled-session data preparation, next-bar open-to-close targets, leakage-aware predictors, and a future-data invariance check.
- `03_baseline_logistic_regression.ipynb`: majority and direction-persistence baselines plus Logistic Regression, evaluated with expanding chronological windows.
- `04_xgboost_lstm.ipynb`: fixed-settings comparison of two simple baselines, Logistic Regression, XGBoost and LSTM; it reads saved results and isolates model fitting in a separate process when results need to be generated.
- `05_long_or_cash_backtest.ipynb`: saved out-of-sample long-or-cash performance using next-bar-open entries and open-to-close returns, with per-side cost sensitivity.
- `06_indicator_ablation.ipynb`: paired comparison of the base predictors with MACD, RSI, Bollinger bandwidth, and session VWAP distance, including matched cost-sensitivity results.

## Planned notebooks

- Review and robustness checks for the trading-strategy evaluation
