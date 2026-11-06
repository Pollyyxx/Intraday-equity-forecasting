# Project Progress Log

## 18 October 2026 — Data Exploration and Preliminary Preparation

### 1. Dataset selection and loading
- Selected SPY and QQQ ETFs as proxies for the S&P 500 and Nasdaq-100.
- Loaded five-minute OHLCV data covering 7 March 2022 to 16 October 2026.
- Confirmed that both datasets contain 1,159 trading dates.
- Checked for missing values, duplicate timestamps, and differences in timestamp coverage between the instruments.

### 2. Data-quality assessment
- Compared observed timestamps with the NYSE trading calendar, including early-close sessions.
- Identified missing five-minute bars in both datasets and observations outside expected market-session times.
- Identified 23 December 2024 as a particularly incomplete session for both ETFs.
- Confirmed that the source is IEX-based and does not represent consolidated trading across all US exchanges.
- Decided to preserve the original data files and perform preliminary filtering in separate research datasets.

### 3. Preliminary dataset preparation
- Created research datasets containing observations within scheduled market sessions.
- Retained valid observations from partially incomplete sessions without filling missing prices.
- Created a binary target representing the direction of the next five-minute close-to-close return.
- Verified that valid targets correspond to consecutive five-minute timestamps within the same trading day.
- Confirmed that targets are not calculated across missing intervals or overnight session boundaries.

### 4. Repository management
- Saved the exploratory notebook, `01_data_availability_and_exploration.ipynb`, to the private GitHub repository.
- Updated `.gitignore` to exclude the local Python environment, notebook checkpoints, and raw CSV/Parquet files.

## 19 October 2026 — Exploratory Analysis and Baseline

### Descriptive analysis

- Summarised the SPY and QQQ research datasets, including closing prices, next-five-minute returns, and trading volume.
- Checked the direction of the next-five-minute returns. The up and down classes were close to evenly balanced for both ETFs.
- Added charts to examine return distributions and how typical returns and trading volume vary during the trading day.

### Majority-class baseline

- Created a simple baseline that predicts the most common direction in the training data.
- Used earlier trading days for training and later days for testing.
- The baseline accuracy was about 50% for both ETFs. This provides a reference point for comparing future models.

### 5. Completed follow-on preparation and model comparison — 21 October 2026
- Finalised a reproducible calendar-based preparation check. The raw Parquet files remain unchanged; the research data keeps observed scheduled bars and does not interpolate missing bars.
- Added next-bar direction targets only when the next observed bar is exactly five minutes later on the same session date.
- Added 11 predictors built from current and past bars. Checked that changing future OHLCV does not alter earlier predictors.
- Added expanding-window validation with a 60% initial training period and five later, chronological test folds.
- Compared a training-period majority baseline, scaled Logistic Regression, XGBoost, and LSTM. All four models use the same test timestamps; rows without 12 uninterrupted five-minute bars are excluded from the shared comparison.
- Fit feature scaling using training rows only. Kept the LSTM sequences within a single session and checked label/timestamp alignment.
- Saved fold metrics and shared-timestamp predictions under `results/advanced_model_fold_metrics.csv` and `results/advanced_model_predictions.csv`.
- The model notebook reads those saved results by default. Heavy model fitting runs in a separate project process, keeping the notebook kernel isolated.

### 6. Long-or-cash backtest — 21 October 2026
- Applied the documented long-or-cash rule to the shared out-of-sample model predictions and their realized next-bar close-to-close returns.
- Compounded strategy returns by session and calculated cumulative net return, maximum drawdown, annualized daily Sharpe, exposure, entries, exits, and one-way turnover.
- Closed positions when the next scored timestamp was unavailable, including session ends and data/sequence gaps.
- Ran illustrative all-in transaction-cost and slippage sensitivities at 0, 1, 2.5, 5, and 10 basis points per side. These are scenario inputs, not estimates of actual trading costs.
- At zero cost, the XGBoost long-or-cash strategy returned about 25% cumulatively on each ETF in the evaluated period; at the illustrative 1 bp per-side scenario, cumulative net returns were about -58% for QQQ and -55% for SPY. The strategy entered roughly 11 times per test session, so turnover makes the result highly cost-sensitive.
- Saved strategy summaries and daily return series under `results/long_or_cash_backtest_summary.csv` and `results/long_or_cash_backtest_daily_returns.csv`.

### 7. Technical-indicator ablation — 21 October 2026
- Compared the existing 11 predictors against the same predictors augmented with MACD line and histogram (normalized by close), 14-period RSI, 20-period Bollinger bandwidth, and distance from session VWAP.
- Kept identical eligible rows, chronological folds, model settings, and test timestamps for the two feature sets. Indicator warm-up observations were excluded from both arms so the comparison is paired.
- Reset rolling MACD/RSI/Bollinger histories at session boundaries and after missing five-minute bars. Session VWAP resets each day and uses only the available IEX source volume. A future-data perturbation check confirmed that changing later bars did not alter earlier indicator values.
- The augmented indicators did not produce a consistent improvement in classification metrics. Mean fold XGBoost ROC-AUC changed from 0.5162 to 0.5157 for QQQ and 0.5229 to 0.5190 for SPY. Mean accuracy changed from 0.5117 to 0.5099 for QQQ and 0.5133 to 0.5125 for SPY. Logistic and LSTM results were mixed across ETF and metric.
- On matched out-of-sample XGBoost predictions, zero-cost cumulative return moved from 13.05% to 14.00% for QQQ and from 9.08% to 10.71% for SPY. At 1 bp per side, both remained negative (-40.03% to -37.26% for QQQ; -42.63% to -39.18% for SPY). This exploratory change does not remove the strategy's high cost sensitivity.
- Saved fold metrics, predictions, metric deltas, and matched cost-sensitivity backtests in `results/indicator_ablation_*.csv`; added `notebooks/06_indicator_ablation.ipynb` to review them.

### 8. Remaining work
- Review model results and confirm final modelling choices.
- Review execution-price assumptions and cost scenarios against the chosen data source and any available broker/venue information.
- Run robustness checks on the strategy and performance metrics.
- Record final methodological decisions and validate the complete analysis before writing dissertation text.


## 6 November 2026 — Execution timing and time-series benchmark review

- Replaced the earlier close-to-close target with the next five-minute bar's open-to-close return. Predictors are available at the current bar close; the simulated position enters at the next bar open and exits at that bar's close. Saved signal, entry and exit timestamps and added checks that the timestamps and return prices agree.
- Added a direction-persistence benchmark that carries the latest completed close-to-close direction forward. Kept the training-majority baseline as a separate benchmark.
- Re-ran the five-fold model comparison for both ETFs. On the full shared comparison, XGBoost mean accuracy / ROC-AUC was 0.5153 / 0.5230 for QQQ and 0.5175 / 0.5283 for SPY. Direction persistence was below 50% accuracy for both ETFs.
- Re-ran the matched indicator ablation. On its smaller warm-up-complete sample, indicators did not improve XGBoost results consistently; this result is only compared within the matched ablation sample.
- Re-ran the long-or-cash backtest. XGBoost zero-cost cumulative return was 37.18% for QQQ and 27.70% for SPY; at the illustrative 1 bp per-side case it was -52.05% and -56.39%. These are sensitivity results under a bar-level execution assumption, not verified broker costs or live-trading evidence.
- The earlier close-to-close backtest outputs in the Git history are superseded by the current outputs.

### Remaining work after this review
- Freeze target, features, models and strategy settings before any final performance evaluation. The existing folds have already been inspected, so do not describe them as a brand-new untouched holdout. If an independent final period is required, collect later data after the method is fixed or clearly explain this limitation.
- Review cost inputs against available spread, fee and execution information; otherwise retain them as explicitly illustrative scenarios.
- Complete robustness analysis, business interpretation and recommendations, visuals, and the student-written report.
- Add or maintain the comprehensive AI coding interaction record and disclosure required by the Handbook.

## 6 November 2026 — Fold-by-fold robustness review

- Added `python_code/run_robustness_checks.py` to assign each saved prediction to its chronological test fold, verify each prediction is assigned once, and confirm assigned row counts match the saved fold sizes.
- Re-ran the existing long-or-cash calculation separately within each fold. Each fold portfolio starts flat and closes any final position at the fold boundary; fold returns are compared as separate periods and are not compounded together.
- Saved fold predictive metrics, fold backtest summaries, daily fold returns, and return-range summaries under `results/robustness_*.csv`. Added `notebooks/07_robustness_checks.ipynb` for reviewing those tables and plotting XGBoost fold returns.
- All 46,951 predictions mapped to one fold, and row counts matched the saved fold definitions. XGBoost was positive in all five zero-cost folds for QQQ (range +5.74% to +7.57%) and SPY (range +0.58% to +9.07%). At the illustrative 1 bp per-side scenario, no XGBoost fold was positive; mean fold returns were -13.67% for QQQ and -15.25% for SPY. Costs are scenario assumptions, and these reused folds are not an independent final test.
- The fold-by-fold method pays to close a position at each fold boundary, so these fold-level returns are intentionally not directly compounded to reproduce the continuous-period backtest summary.
