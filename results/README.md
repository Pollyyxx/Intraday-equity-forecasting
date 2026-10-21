# Results

This folder contains model evaluation outputs and, in later stages, trading strategy results and backtesting summaries.

- `advanced_model_fold_metrics.csv`: fold-level accuracy, balanced accuracy, F1 and ROC-AUC for the four classification approaches.
- `advanced_model_predictions.csv`: out-of-sample predictions, realized next-bar returns and shared test timestamps used for model comparison and backtesting.
- `long_or_cash_backtest_summary.csv`: cumulative net return, maximum drawdown, annualized daily Sharpe, exposure, turnover and trading activity by model and cost scenario.
- `long_or_cash_backtest_daily_returns.csv`: daily gross and net returns for each model/cost scenario.
- `indicator_ablation_fold_metrics.csv` and `indicator_ablation_summary.csv`: five-fold metrics for base features and base-plus-indicator feature sets.
- `indicator_ablation_deltas.csv`: augmented-minus-base mean-fold metric differences.
- `indicator_ablation_predictions.csv`: paired, shared-timestamp predictions for both feature sets.
- `indicator_ablation_backtest_summary.csv` and `indicator_ablation_backtest_daily_returns.csv`: matched long-or-cash results for both feature sets across the existing per-side cost scenarios.

To recompute the fixed XGBoost/LSTM comparison, run `python_code/run_advanced_models.py` from the project root. The notebook reads the saved outputs by default and does not retrain models when they are already present.

To recompute the long-or-cash results from saved predictions, run `python_code/run_backtest.py`. Cost scenarios are illustrative all-in transaction-cost and slippage rates per side, not broker-specific estimates.

To recompute the indicator ablation, run `python_code/run_indicator_ablation.py` in the project environment. It leaves the original baseline model and backtest outputs unchanged.
