"""Long-or-cash backtesting on chronological out-of-sample predictions."""

from __future__ import annotations

import numpy as np
import pandas as pd


MODEL_PREDICTION_COLUMNS = {
    "Majority baseline": "baseline_prediction",
    "Logistic regression": "logistic_prediction",
    "XGBoost": "xgboost_prediction",
    "LSTM": "lstm_prediction",
}


def _daily_returns(intervals: pd.DataFrame, return_column: str) -> pd.DataFrame:
    return (
        intervals.groupby("session_date", sort=True)[return_column]
        .apply(lambda values: (1 + values).prod() - 1)
        .rename(return_column)
        .reset_index()
    )


def _performance_summary(daily: pd.DataFrame) -> dict[str, float]:
    net = daily["net_return"].to_numpy(dtype=float)
    equity = np.cumprod(1 + net)
    running_peak = np.maximum.accumulate(np.r_[1.0, equity])[1:]
    standard_deviation = daily["net_return"].std(ddof=1)
    sharpe = (
        daily["net_return"].mean() / standard_deviation * np.sqrt(252)
        if len(daily) > 1 and standard_deviation > 0
        else np.nan
    )
    return {
        "sessions": int(len(daily)),
        "gross_cumulative_return": float((1 + daily["gross_return"]).prod() - 1),
        "net_cumulative_return": float(equity[-1] - 1),
        "maximum_drawdown": float(np.min(equity / running_peak - 1)),
        "annualized_daily_sharpe": float(sharpe),
    }


def backtest_long_or_cash(
    predictions: pd.DataFrame,
    cost_bps_per_side=(0.0, 1.0, 2.5, 5.0, 10.0),
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Evaluate one-bar long-or-cash positions with explicit per-side costs.

    Each prediction sets the position for the following close-to-close return.
    Costs apply when the position changes at a signal timestamp. Any position
    with no immediately following scored timestamp is closed at the end of its
    target interval, including session ends and data/sequence gaps.
    """
    required = {
        "ETF", "datetime", "next_datetime", "next_return", "actual",
        *MODEL_PREDICTION_COLUMNS.values(),
    }
    missing = required.difference(predictions.columns)
    if missing:
        raise ValueError(f"Missing backtest columns: {sorted(missing)}")
    if not cost_bps_per_side or any(cost < 0 for cost in cost_bps_per_side):
        raise ValueError("cost_bps_per_side must contain non-negative values")

    data = predictions.copy()
    data["datetime"] = pd.to_datetime(data["datetime"], errors="raise")
    data["next_datetime"] = pd.to_datetime(data["next_datetime"], errors="raise")
    data["next_return"] = pd.to_numeric(data["next_return"], errors="raise")
    data = data.sort_values(["ETF", "datetime"], kind="stable").reset_index(drop=True)
    if data.duplicated(["ETF", "datetime"]).any():
        raise ValueError("Each ETF must have at most one prediction per timestamp")
    if not np.isfinite(data["next_return"]).all() or (data["next_return"] <= -1).any():
        raise ValueError("next_return must be finite and greater than -100%")
    if not np.array_equal((data["next_return"] > 0).astype(int), data["actual"].astype(int)):
        raise AssertionError("Saved direction labels do not match realized next-bar returns")
    if not (data["next_datetime"] - data["datetime"]).eq(pd.Timedelta(minutes=5)).all():
        raise AssertionError("Backtest targets must end at the next five-minute timestamp")
    if not (data["datetime"].dt.date == data["next_datetime"].dt.date).all():
        raise AssertionError("Backtest targets must not cross session dates")

    summaries = []
    daily_parts = []
    for ticker, ticker_data in data.groupby("ETF", sort=True):
        ticker_data = ticker_data.sort_values("datetime", kind="stable").copy()
        session_dates = ticker_data["datetime"].dt.date
        for model_name, prediction_column in MODEL_PREDICTION_COLUMNS.items():
            positions = ticker_data[prediction_column].astype(int)
            if not positions.isin([0, 1]).all():
                raise ValueError(f"{ticker}/{model_name} predictions must be binary")

            position_by_time = dict(zip(ticker_data["datetime"], positions))
            preceding_position = ticker_data["datetime"].map(
                dict(zip(ticker_data["next_datetime"], positions))
            ).fillna(0).astype(int)
            next_position = ticker_data["next_datetime"].map(position_by_time)
            has_next_score = next_position.notna()

            entry_turnover = (positions - preceding_position).abs()
            forced_exit_turnover = positions.where(~has_next_score, 0)
            turnover = entry_turnover + forced_exit_turnover
            gross_strategy_return = positions.to_numpy() * ticker_data["next_return"].to_numpy()

            # Costs are an explicit scenario input, not a claim about actual brokerage fees.
            for cost_bps in cost_bps_per_side:
                cost_fraction = float(cost_bps) / 10_000
                entry_cost = entry_turnover.to_numpy() * cost_fraction
                exit_cost = forced_exit_turnover.to_numpy() * cost_fraction
                intervals = pd.DataFrame({
                    "ETF": ticker,
                    "model": model_name,
                    "datetime": ticker_data["datetime"].to_numpy(),
                    "next_datetime": ticker_data["next_datetime"].to_numpy(),
                    "session_date": session_dates.to_numpy(),
                    "position": positions.to_numpy(),
                    "asset_return": ticker_data["next_return"].to_numpy(),
                    "gross_return": gross_strategy_return,
                    "entry_turnover": entry_turnover.to_numpy(),
                    "exit_turnover": forced_exit_turnover.to_numpy(),
                    "one_way_turnover": turnover.to_numpy(),
                    "entry_cost": entry_cost,
                    "exit_cost": exit_cost,
                })
                intervals["net_return"] = (
                    (1 - intervals["entry_cost"])
                    * (1 + intervals["gross_return"])
                    * (1 - intervals["exit_cost"])
                    - 1
                )
                daily = _daily_returns(intervals, "gross_return").merge(
                    _daily_returns(intervals, "net_return"), on="session_date", validate="one_to_one"
                )
                daily.insert(0, "ETF", ticker)
                daily.insert(1, "model", model_name)
                daily.insert(2, "cost_bps_per_side", float(cost_bps))
                daily_parts.append(daily)

                summary = {
                    "ETF": ticker,
                    "model": model_name,
                    "cost_bps_per_side": float(cost_bps),
                    "intervals": int(len(intervals)),
                    "active_intervals": int(positions.sum()),
                    "exposure_fraction": float(positions.mean()),
                    "entries": int(((positions == 1) & (preceding_position == 0)).sum()),
                    "exits": int(((positions == 0) & (preceding_position == 1)).sum() + forced_exit_turnover.sum()),
                    "trade_events": int(turnover.sum()),
                    "one_way_turnover": float(turnover.sum()),
                    "entries_per_session": float(
                        ((positions == 1) & (preceding_position == 0)).sum() / session_dates.nunique()
                    ),
                    "cumulative_cost_fraction_uncompounded": float(
                        intervals["entry_cost"].sum() + intervals["exit_cost"].sum()
                    ),
                    **_performance_summary(daily),
                }
                summaries.append(summary)

    return pd.DataFrame(summaries), pd.concat(daily_parts, ignore_index=True)
