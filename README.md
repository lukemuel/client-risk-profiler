# Client Risk Profiler

A staged tool that takes a client's profile (age, time horizon, income stability, loss tolerance) and matches them to a model investment portfolio — then backtests that portfolio against real historical market data so the risk/return tradeoff is concrete, not theoretical.

Built to demonstrate the kind of risk assessment and client communication work involved in a financial advisory / brokerage role.

## What it does

1. **Scores a client's risk tolerance** (0-100) from a short intake questionnaire
2. **Matches them to a model portfolio** — Conservative, Moderate, or Aggressive — built from real ETFs (BND, VOO, VXUS)
3. **Backtests that portfolio** against actual 2018-2024 market data, including the 2018 selloff, 2020 COVID crash, and 2022 bear market
4. **Generates a plain-English client report** — no jargon, just "here's what your money would have done, including the worst stretch"

## Example Output
## Model Portfolio Results (2018-2024 backtest)

| Risk Level | Allocation | Avg Annual Return | Volatility | Max Drawdown |
|---|---|---|---|---|
| Conservative | 65% Bonds / 25% US Stocks / 10% Intl | 4.8% | 8.2% | -18.9% |
| Moderate | 40% Bonds / 45% US Stocks / 15% Intl | 7.5% | 12.0% | -21.9% |
| Aggressive | 10% Bonds / 65% US Stocks / 25% Intl | 10.1% | 17.0% | -30.9% |

## Staged Build

- **Stage 1:** Client intake questionnaire → 0-100 risk score → risk bucket (`src/stage1_risk_score.py`)
- **Stage 2:** Model portfolio definitions per risk bucket using real ETFs (`src/stage2_model_portfolios.py`)
- **Stage 3:** Historical backtest of each model portfolio, 2018-2024 (`src/stage3_backtest.py`)
- **Stage 4:** Plain-English client report generator (`src/stage4_client_report.py`)
- **Stage 5:** Full pipeline — client intake flows directly into a matched, backtested report (`src/stage5_full_flow.py`)

## Tech Stack

- **pandas / numpy** — data wrangling and return/risk calculations
- **yfinance** — real historical ETF price data

## Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

python src/stage5_full_flow.py
```

## Status

✅ Complete — full pipeline from client intake to backtested, plain-English report.
