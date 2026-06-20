"""
Stage 5: Full Client Flow (Intake -> Risk Score -> Matched Portfolio Report)
--------------------------------------------------------------------------------
Goal: tie the risk scoring system directly to the model portfolio
report generator, so a client's answers flow into their final report.
"""

import yfinance as yf
import numpy as np
import pandas as pd

# -----------------------------
# 1. Risk scoring functions (from Stage 1)
# -----------------------------
def score_age(age):
    if age < 35:
        return 25
    elif age < 50:
        return 18
    elif age < 65:
        return 10
    else:
        return 4

def score_time_horizon(years_until_needed):
    if years_until_needed >= 20:
        return 25
    elif years_until_needed >= 10:
        return 18
    elif years_until_needed >= 5:
        return 10
    else:
        return 4

def score_income_stability(stability):
    mapping = {"stable": 20, "somewhat_stable": 12, "unstable": 5}
    return mapping.get(stability, 10)

def score_loss_tolerance(reaction):
    mapping = {"buy_more": 30, "hold": 22, "sell_some": 10, "sell_all": 0}
    return mapping.get(reaction, 15)

def calculate_risk_score(age, years_until_needed, income_stability, loss_reaction):
    return (
        score_age(age)
        + score_time_horizon(years_until_needed)
        + score_income_stability(income_stability)
        + score_loss_tolerance(loss_reaction)
    )

def get_risk_bucket(score):
    if score >= 70:
        return "Aggressive"
    elif score >= 45:
        return "Moderate"
    else:
        return "Conservative"

# -----------------------------
# 2. Model portfolios + descriptions (from Stage 4)
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

asset_names = {"BND": "Bonds", "VOO": "U.S. Stocks", "VXUS": "International Stocks"}

# -----------------------------
# 3. Pull historical data once (reused for any client)
# -----------------------------
tickers = ["BND", "VOO", "VXUS"]
start_date = "2018-01-01"
end_date = "2024-12-31"

raw_data = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True, threads=False)
prices = raw_data["Close"].ffill().dropna()
daily_returns = prices.pct_change().dropna()

def get_backtest_stats(risk_level):
    allocation = model_portfolios[risk_level]
    weights = np.array([allocation[t] for t in tickers])
    portfolio_returns = daily_returns[tickers].dot(weights)

    cumulative = (1 + portfolio_returns).cumprod()
    total_return = cumulative.iloc[-1] - 1
    annualized_return = (1 + total_return) ** (252 / len(portfolio_returns)) - 1
    annual_vol = portfolio_returns.std() * np.sqrt(252)

    running_max = cumulative.cummax()
    drawdown = (cumulative - running_max) / running_max
    max_drawdown = drawdown.min()

    return total_return, annualized_return, annual_vol, max_drawdown

# -----------------------------
# 4. Full client intake -> report function
# -----------------------------
def generate_client_report(client_name, age, years_until_needed, income_stability, loss_reaction):
    score = calculate_risk_score(age, years_until_needed, income_stability, loss_reaction)
    risk_level = get_risk_bucket(score)
    allocation = model_portfolios[risk_level]
    total_return, annualized_return, annual_vol, max_drawdown = get_backtest_stats(risk_level)

    print("=" * 60)
    print(f"  CLIENT REPORT: {client_name}")
    print("=" * 60)
    print(f"\nRisk Score: {score}/100  ->  Matched Profile: {risk_level}\n")
    print(descriptions[risk_level])
    print("\nRecommended Allocation:")
    for ticker, weight in allocation.items():
        print(f"  • {asset_names[ticker]}: {weight:.0%}")

    print(f"\nHistorical performance (2018-2024):")
    print(f"  • Average annual return: {annualized_return:.1%}")
    print(f"  • Typical volatility: {annual_vol:.1%}")
    print(f"  • Worst historical drop: {max_drawdown:.1%}")

    print(f"\nWhat this means: $10,000 invested in 2018 would have grown to "
          f"${10000 * (1 + total_return):,.0f} by 2024, with a worst-case drop of "
          f"{abs(max_drawdown):.0%} along the way.\n")

# -----------------------------
# 5. Example: run a few fake clients through the full pipeline
# -----------------------------
generate_client_report(
    client_name="Sarah Thompson",
    age=29,
    years_until_needed=25,
    income_stability="stable",
    loss_reaction="hold",
)

generate_client_report(
    client_name="Robert Kim",
    age=58,
    years_until_needed=5,
    income_stability="somewhat_stable",
    loss_reaction="sell_some",
)
