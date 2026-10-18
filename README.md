# Machine Learning for Intraday Equity Index Forecasting

## Project Overview

This project investigates whether machine learning models can predict short-term price movements in major US equity markets and whether these predictions can support a profitable trading strategy.

## Research Question

Can selected machine learning models predict the next five-minute price direction of SPY and QQQ, and do their predictions generate better trading performance after transaction costs and slippage?

## Instruments and Data

- SPY: S&P 500 ETF
- QQQ: Nasdaq-100 ETF
- Frequency: Five-minute OHLCV data
- Historical period: To be determined after data availability checks

## Models

1. Naive forecasting baseline
2. Logistic Regression
3. XGBoost
4. Long Short-Term Memory (LSTM)

## Methodology

- Data cleaning and feature engineering
- Expanding-window walk-forward validation
- Out-of-sample predictive evaluation
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
- data/: Dataset documentation
- results/: Charts and evaluation results
- docs/: Research documentation and methodology notes

## Project Status

Currently setting up the research environment and verifying historical data availability.
