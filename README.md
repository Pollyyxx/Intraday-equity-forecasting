# Machine Learning for Intraday Equity Index Forecasting

## Project Overview

This project investigates whether machine learning models can predict short-term price movements in major US equity markets and whether these predictions can support a profitable trading strategy.

## Research Question

Can selected models predict the next five-minute bar’s open-to-close direction for SPY and QQQ, and how does a long-or-cash strategy perform under explicit transaction-cost and slippage scenarios?

## Instruments and Data

- SPY: S&P 500 ETF
- QQQ: Nasdaq-100 ETF
- Frequency: Five-minute OHLCV data
- Historical period: 7 March 2022 to 16 October 2026 in the current source files

## Models

1. Majority-class baseline
2. Direction-persistence time-series baseline
3. Logistic Regression
4. XGBoost
5. Long Short-Term Memory (LSTM)

## Methodology

- Data cleaning and feature engineering
- Expanding-window walk-forward validation
- Out-of-sample predictive evaluation
- Signal after completed bar; hypothetical entry at the next bar open and exit at that bar close
- Long-or-cash trading strategy
- Backtesting with transaction costs and slippage

## Evaluation Metrics

Predictive metrics:
- Directional accuracy
- F1-score
- ROC-AUC

Financial metrics:
- Cumulative net return
- Maximum drawdown
- Sharpe ratio
- Trading frequency and turnover

## Project Structure

- `01_data_availability_and_exploration.ipynb`: initial data-quality checks and EDA.
- notebooks/: Feature engineering, modelling, backtesting, and robustness analyses
- python_code/: Reusable Python functions
- data/: Dataset notes; the local CSV and Parquet data files are excluded from Git
- results/: Charts and evaluation results
- docs/: Research documentation and methodology notes

## Reproducing the analysis

Use Python 3.13 and install the packages in `requirements.txt`. Keep the cleaned input files `QQQ_clean_5min.parquet` and `SPY_clean_5min.parquet` in `data/`; they are not included in Git. See `data/README.md` for the data note.

From the project root, run `python python_code/run_advanced_models.py`, then `python python_code/run_backtest.py`, `python python_code/run_indicator_ablation.py`, and `python python_code/run_robustness_checks.py`. The model runner keeps XGBoost and PyTorch work in a separate process from notebook kernels.

## Project Status

- Data: SPY and QQQ five-minute bars from 7 March 2022 to 16 October 2026.
- Models: majority and direction-persistence baselines, Logistic Regression, XGBoost, and LSTM.
- Trading rule: each positive forecast is a separate trade from the next bar open to its close. Costs are charged at entry and exit.
- Evaluation: five expanding chronological folds. These folds have already informed model review, so they are not an untouched final test.
- Limits: costs are illustrative, and the source data does not include quotes or actual fills.
- Results: notebooks 07 and 08 review fold stability, model scores, cost sensitivity, and the indicator ablation.
- Remaining work: write the report independently, confirm examiner access to the licensed data, and complete the activity record and required declarations.
