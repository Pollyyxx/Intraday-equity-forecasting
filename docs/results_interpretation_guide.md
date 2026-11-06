# Results interpretation evidence map

This is a working guide to the saved outputs, not dissertation text. Use the questions to develop your own interpretation and business recommendation. Values below are a snapshot from the saved results on 6 November 2026; refresh them if the model outputs are rerun.

## 1. Study and evaluation frame

- Instruments and frequency: SPY and QQQ, five-minute OHLCV bars.
- Available dates: 7 March 2022 to 16 October 2026. The local source is IEX-based, not consolidated US-market volume.
- Target: the next five-minute bar's open-to-close direction, predicted after the current bar has completed.
- Evaluation: five expanding chronological folds and 46,951 shared out-of-sample prediction rows.
- Important boundary: these folds have already informed model review. Describe them as walk-forward folds, not an untouched final holdout.
- Execution assumption: enter at the next bar open and exit at its close. Cost values are illustrative because the source files contain no bid/ask quotes, order details or fills.

## 2. Predictive results

Mean accuracy and standard deviation are across five test folds. Accuracy lift is measured against the majority baseline for the same ETF. Baselines provide hard labels only, so ROC-AUC is not available for them.

| ETF | Model | Mean accuracy ± fold SD | Mean ROC-AUC | Accuracy lift vs majority |
|---|---|---:|---:|---:|
| QQQ | Majority baseline | 50.55% ± 0.34 pp | — | 0.00 pp |
| QQQ | Direction-persistence baseline | 48.13% ± 1.41 pp | — | −2.42 pp |
| QQQ | Logistic Regression | 50.75% ± 0.73 pp | 0.5135 | +0.19 pp |
| QQQ | XGBoost | 51.53% ± 1.04 pp | 0.5230 | +0.98 pp |
| QQQ | LSTM | 51.42% ± 0.69 pp | 0.5192 | +0.86 pp |
| SPY | Majority baseline | 50.42% ± 0.86 pp | — | 0.00 pp |
| SPY | Direction-persistence baseline | 47.89% ± 0.98 pp | — | −2.53 pp |
| SPY | Logistic Regression | 51.30% ± 0.87 pp | 0.5195 | +0.88 pp |
| SPY | XGBoost | 51.75% ± 1.14 pp | 0.5283 | +1.33 pp |
| SPY | LSTM | 51.32% ± 1.33 pp | 0.5258 | +0.90 pp |

**Questions for your interpretation**

- How large are the accuracy lifts in practical terms, and how consistent are they across the five folds?
- Do the AUC and balanced-accuracy results support the same reading as raw accuracy?
- What does the persistence baseline add to the comparison?

Source: `results/advanced_model_fold_metrics.csv`; see [notebook 03](../notebooks/03_baseline_logistic_regression.ipynb) and [notebook 04](../notebooks/04_xgboost_lstm.ipynb).

## 3. Strategy results and trading activity

XGBoost is shown below as the strongest mean-accuracy model in this saved comparison. Returns are from the continuous-period backtest; maximum drawdown and annualized daily Sharpe are calculated from its daily net returns.

| ETF | Cost per side | Net cumulative return | Maximum drawdown | Annualized daily Sharpe | Entries per session | Exposure | One-way position changes |
|---|---:|---:|---:|---:|---:|---:|---:|
| QQQ | 0 bp | +37.18% | −6.30% | 2.25 | 11.33 | 63.4% | 10,512 |
| QQQ | 1 bp | −52.05% | −52.05% | −5.14 | 11.33 | 63.4% | 10,512 |
| SPY | 0 bp | +27.70% | −8.72% | 1.77 | 11.58 | 64.1% | 10,744 |
| SPY | 1 bp | −56.39% | −56.39% | −5.90 | 11.58 | 64.1% | 10,744 |

All five model and baseline strategies have negative continuous-period net returns at the illustrative 1 bp-per-side case for both ETFs. Entries per session and one-way position changes do not vary across cost rows because the saved signals are fixed. One-way position changes count the entries and exits in this long-or-cash setup; costs are applied at those changes. The 0 bp row is a gross reference, not a likely real-world outcome.

**Questions for your interpretation**

- Why does a small predictive lift fail to guarantee a positive trading result?
- How does the frequency of position changes interact with per-side costs?
- What can you conclude conditionally from the 1 bp case, given that the rate is not calibrated from quote or broker data?

Source: `results/model_strategy_comparison.csv` and `results/long_or_cash_backtest_summary.csv`; see [notebook 05](../notebooks/05_long_or_cash_backtest.ipynb) and [notebook 08](../notebooks/08_results_review.ipynb).

## 4. Fold-to-fold strategy stability

Each fold is reviewed as a separate portfolio that starts and ends flat. Fold returns are not compounded together and are not the same calculation as the continuous-period results above.

| ETF | Cost per side | Positive XGBoost folds | Mean fold return | Range across folds |
|---|---:|---:|---:|---:|
| QQQ | 0 bp | 5 of 5 | +6.53% | +5.74% to +7.57% |
| QQQ | 1 bp | 0 of 5 | −13.67% | −14.60% to −12.05% |
| SPY | 0 bp | 5 of 5 | +5.06% | +0.58% to +9.07% |
| SPY | 1 bp | 0 of 5 | −15.25% | −18.76% to −12.12% |

**Questions for your interpretation**

- What does the repeated sign across folds show, and what does it not establish?
- Why should the fold-level results remain separate from the continuous-period compounded backtest?

Source: `results/robustness_backtest_stability.csv`; see [notebook 07](../notebooks/07_robustness_checks.ipynb).

## 5. Technical-indicator ablation

The comparison adds MACD, RSI, Bollinger bandwidth and session VWAP distance to the base predictors. It uses the same matched, warm-up-complete rows for both feature sets, so its absolute scores should not be compared directly with the full-sample model results.

| ETF | XGBoost accuracy change | XGBoost ROC-AUC change |
|---|---:|---:|
| QQQ | −0.25 pp | −0.62 pp |
| SPY | −0.02 pp | −0.20 pp |

**Questions for your interpretation**

- Did these indicators add predictive value on the matched sample?
- Does the ablation support treating the indicators as a secondary analysis rather than a core result?

Source: `results/indicator_ablation_deltas.csv`; see [notebook 06](../notebooks/06_indicator_ablation.ipynb).

## 6. Visuals to consider in the report

- Data quality and missing-session bars: [notebook 01](../01_data_availability_and_exploration.ipynb).
- Mean model scores and fold spread: [notebook 04](../notebooks/04_xgboost_lstm.ipynb).
- Cost-sensitive equity curves: [notebook 05](../notebooks/05_long_or_cash_backtest.ipynb).
- Separate fold returns: [notebook 07](../notebooks/07_robustness_checks.ipynb).
- Entries per session and signal-to-execution comparison: [notebook 08](../notebooks/08_results_review.ipynb).
- Indicator change plot: [notebook 06](../notebooks/06_indicator_ablation.ipynb), if it supports the final scope.

Choose figures that answer a question in the report; avoid showing several versions of the same result.

## 7. Business-decision prompts

Before writing the report in your own words, decide:

1. What decision would a business stakeholder need to make from a five-minute directional signal?
2. Is the observed predictive improvement sufficient to justify further investigation, given fold variation and the cost-sensitive returns?
3. What evidence is still missing before any deployment claim could be made?
4. How should the conclusions be limited by IEX-only volume, the bar-level execution assumption, the lack of quote-based costs, and the absence of a later untouched test period?

Use the evidence above to answer these questions yourself. Do not present the illustrative cost grid as a measured broker cost or the reviewed folds as a new independent holdout.
