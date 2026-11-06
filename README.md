# Machine Learning for Intraday Equity Index Forecasting

## Project Overview

This project investigates whether machine learning models can predict short-term price movements in major US equity markets and whether these predictions can support a profitable trading strategy.

## Research Question

Can selected models predict the next five-minute bar’s open-to-close direction for SPY and QQQ, and can those predictions support a long-or-cash strategy after transaction costs and slippage?

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

- notebooks/: Data analysis and model experiments
- python_code/: Reusable Python functions
- data/: Dataset notes; the local CSV and Parquet data files are excluded from Git
- results/: Charts and evaluation results
- docs/: Research documentation and methodology notes

## Reproducing the analysis

Use Python 3.13 and install the packages in `requirements.txt`. Keep the cleaned input files `QQQ_clean_5min.parquet` and `SPY_clean_5min.parquet` in `data/`; they are not included in Git. See `data/README.md` for the data note.

From the project root, run `python python_code/run_advanced_models.py`, then `python python_code/run_backtest.py`, `python python_code/run_indicator_ablation.py`, and `python python_code/run_robustness_checks.py`. The model runner keeps XGBoost and PyTorch work in a separate process from notebook kernels.

## Project Status

The analysis now uses a next-bar-open entry assumption: after the current five-minute bar closes, each signal is evaluated on the following bar's open-to-close direction. It compares the training-majority baseline, direction-persistence baseline, Logistic Regression, XGBoost and LSTM. The refreshed backtest remains highly sensitive to the illustrative per-side cost scenarios. Fold-by-fold robustness outputs are available in `results/robustness_*.csv` and reviewed in `notebooks/07_robustness_checks.ipynb`. These are stability checks on folds already used for model review, not an untouched final test. A final business interpretation and the student-written report remain to be completed.
