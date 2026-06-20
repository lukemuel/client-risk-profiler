"""
Stage 4: Client-Facing Report
-----------------------------------
Goal: generate a clean, plain-English summary report
per risk profile, combining backtest results with
client-friendly explanations.
"""

import yfinance as yf
import numpy as np
import pandas as pd

# -----------------------------
# 1. Model portfolios + descriptions
# -----------------------------
model_portfolios = {
    "Conservative": {"BND": 0.65, "VOO": 0.25, "VXUS": 0.10},
    "Moderate": {"BND": 0.40, "VOO": 0.45, "VXUS": 0.15},
    "Aggressive": {"BND": 0.10, "VOO": 0.65, "VXUS": 0.25},
}

descriptions = {
    "Conservative": "Built for clients who prioritize protecting their money over maximizing "
                    "growth. Most of the portfolio sits in bonds, which tend to hold steadier "
                    "during stock market downturns.",
    "Moderate": "A balanced approach — roughly half bonds, half stocks. Designed for clients "
                "who want meaningful growth but aren't comfortable with the full swings of an "
                "all-stock portfolio.",
    "Aggressive": "Built for clients with a long time horizon who can ride out short-term "
                  "losses in exchange for higher long-term growth potential. Mostly stocks, "
                  "minimal bonds.",
}

tickers = ["BND", "VOO", "VXUS"]
start_date = "2018-01-01"
end_date = "2024-12-31"

# -----------------------------
# 2. Pull data + run backtest (same as Stage 3)
# -----------------------------
raw_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, threads=False)
prices = raw_data["Close"].ffill().dropna()
daily_returns = prices.pct_change().dropna()

report_data = {}

for risk_level, allocation in model_portfolios.items():
    weights = np.array([allocation[t] for t in tickers])
    portfolio_returns = daily_returns[tickers].dot(weights)

    cumulative = (1 + portfolio_returns).cumprod()
    total_return = cumulative.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (252 / len(portfolio_returns)) - 1
    annual_vol = portfolio_returns.std() * np.sqrt(252)

    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    yearly_returns = portfolio_returns.resample('YE').apply(lambda x: (1 + x).prod() - 1)
    worst_year = yearly_returns.min()
    worst_year_date = yearly_returns.idxmin().year
    best_year = yearly_returns.max()
    best_year_date = yearly_returns.idxmax().year

    report_data[risk_level] = {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annual_vol": annual_vol,
        "max_drawdown": max_drawdown,
        "worst_year": worst_year,
        "worst_year_date": worst_year_date,
        "best_year": best_year,
        "best_year_date": best_year_date,
    }

# -----------------------------
# 3. Generate client-friendly report per risk profile
# -----------------------------
def print_client_report(risk_level):
    d = report_data[risk_level]
    allocation = model_portfolios[risk_level]

    print("=" * 60)
    print(f"  PORTFOLIO PROFILE: {risk_level.upper()}")
    print("=" * 60)
    print(f"\n{descriptions[risk_level]}\n")

    print("Allocation:")
    asset_names = {"BND": "Bonds", "VOO": "U.S. Stocks", "VXUS": "International Stocks"}
    for ticker, weight in allocation.items():
        print(f"  • {asset_names[ticker]}: {weight:.0%}")

    print(f"\nHistorical performance (2018-2024, based on real market data):")
    print(f"  • Average annual return: {d['annualized_return']:.1%} per year")
    print(f"  • Typical year-to-year swing (volatility): {d['annual_vol']:.1%}")
    print(f"  • Worst stretch (peak to trough): {d['max_drawdown']:.1%}")
    print(f"  • Best calendar year: {d['best_year']:.1%} ({d['best_year_date']})")
    print(f"  • Worst calendar year: {d['worst_year']:.1%} ({d['worst_year_date']})")

    print(f"\nWhat this means for you:")
    print(f"  If you invested $10,000 in this strategy in 2018, it would have grown to "
          f"approximately ${10000 * (1 + d['total_return']):,.0f} by the end of 2024 — "
          f"but along the way, you would have seen your account value drop as much as "
          f"{abs(d['max_drawdown']):.0%} at its worst point before recovering.")
    print()

for risk_level in model_portfolios.keys():
    print_client_report(risk_level)
