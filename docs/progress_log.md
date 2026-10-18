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

### 5. Remaining work
- Finalise and document the data-cleaning policy.
- Complete and validate predictive feature engineering.
- Establish expanding-window walk-forward validation.
- Implement and compare the naive baseline, Logistic Regression, XGBoost, and LSTM models.
- Evaluate predictive performance and trading-strategy performance, accounting for transaction costs and slippage.
