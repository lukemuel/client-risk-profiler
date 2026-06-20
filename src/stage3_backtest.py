"""
Stage 3: Historical Backtest
---------------------------------
Goal: pull real historical data for each model portfolio's
ETFs and show actual historical performance and risk per risk bucket.
"""

import yfinance as yf
import numpy as np
import pandas as pd

# -----------------------------
# 1. Define model portfolios (same as Stage 2)
# -----------------------------
model_portfolios = {
    "Conservative": {"BND": 0.65, "VOO": 0.25, "VXUS": 0.10},
    "Moderate": {"BND": 0.40, "VOO": 0.45, "VXUS": 0.15},
    "Aggressive": {"BND": 0.10, "VOO": 0.65, "VXUS": 0.25},
}

tickers = ["BND", "VOO", "VXUS"]
start_date = "2018-01-01"  # longer window to capture 2018, 2020, and 2022 downturns
end_date = "2024-12-31"

# -----------------------------
# 2. Download historical data
# -----------------------------
raw_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, threads=False)
prices = raw_data["Close"].ffill().dropna()
daily_returns = prices.pct_change().dropna()

print(f"Data range: {prices.index.min().date()} to {prices.index.max().date()}")
print(f"Total trading days: {len(prices)}\n")

# -----------------------------
# 3. Calculate performance for each model portfolio
# -----------------------------
results = {}

print("=== HISTORICAL BACKTEST RESULTS (2018-2024) ===\n")

for risk_level, allocation in model_portfolios.items():
    weights = np.array([allocation[t] for t in tickers])
    portfolio_returns = daily_returns[tickers].dot(weights)

    # Total return over the full period
    cumulative = (1 + portfolio_returns).cumprod()
    total_return = cumulative.iloc[-1] - 1

    # Annualized volatility
    annual_vol = portfolio_returns.std() * np.sqrt(252)

    # Max drawdown
    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()
    max_dd_date = drawdown.idxmin()

    # Best and worst calendar year (rough, using yearly resampling)
    yearly_returns = portfolio_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)

    results[risk_level] = {
        "total_return": total_return,
        "annual_vol": annual_vol,
        "max_drawdown": max_drawdown,
        "max_dd_date": max_dd_date,
        "yearly_returns": yearly_returns,
    }

    print(f"--- {risk_level} Portfolio ---")
    print(f"Total return (2018-2024): {total_return:.1%}")
    print(f"Annualized volatility: {annual_vol:.1%}")
    print(f"Max drawdown: {max_drawdown:.1%} (on {max_dd_date.date()})")
    print(f"Worst calendar year: {yearly_returns.min():.1%} ({yearly_returns.idxmin().year})")
    print(f"Best calendar year: {yearly_returns.max():.1%} ({yearly_returns.idxmax().year})")
    print()

# -----------------------------
# 4. Side-by-side comparison table
# -----------------------------
print("=== SIDE-BY-SIDE COMPARISON ===\n")
print(f"{'Risk Level':<14}{'Total Return':<15}{'Volatility':<13}{'Max Drawdown':<15}")
for risk_level, r in results.items():
    print(f"{risk_level:<14}{r['total_return']:<15.1%}{r['annual_vol']:<13.1%}{r['max_drawdown']:<15.1%}")
