"""
Stage 2: Model Portfolios
-----------------------------
Goal: define real, investable model portfolios for each
risk bucket using broad ETFs as proxies.
"""

# -----------------------------
# 1. Define model portfolios by risk bucket
# -----------------------------
# Using simple, well-known ETFs as proxies:
# VOO = S&P 500 (US large-cap stocks)
# BND = Total US bond market
# VXUS = International stocks (diversification beyond US)

model_portfolios = {
    "Conservative": {
        "BND": 0.65,   # mostly bonds — capital preservation focus
        "VOO": 0.25,
        "VXUS": 0.10,
    },
    "Moderate": {
        "BND": 0.40,
        "VOO": 0.45,
        "VXUS": 0.15,
    },
    "Aggressive": {
        "BND": 0.10,   # minimal bonds — growth focus
        "VOO": 0.65,
        "VXUS": 0.25,
    },
}

# -----------------------------
# 2. Validate weights sum to 1.0 for each portfolio
# -----------------------------
print("=== MODEL PORTFOLIO ALLOCATIONS ===\n")
for risk_level, allocation in model_portfolios.items():
    total_weight = sum(allocation.values())
    print(f"{risk_level} Portfolio:")
    for ticker, weight in allocation.items():
        print(f"  {ticker}: {weight:.0%}")
    print(f"  Total: {total_weight:.0%} {'✓' if abs(total_weight - 1.0) < 0.001 else '✗ ERROR'}")
    print()

# -----------------------------
# 3. Plain-English description per portfolio
# -----------------------------
descriptions = {
    "Conservative": "Prioritizes capital preservation. Heavy bond allocation cushions "
                    "against stock market swings, sacrificing some growth potential for stability.",
    "Moderate": "Balanced growth and stability. Roughly even split between stocks and bonds, "
                "designed for clients with a medium time horizon and moderate risk tolerance.",
    "Aggressive": "Growth-focused. Minimal bond exposure, heavily weighted toward equities "
                  "for maximum long-term growth potential, accepting larger short-term swings.",
}

print("=== PLAIN-ENGLISH DESCRIPTIONS (for client conversations) ===\n")
for risk_level, desc in descriptions.items():
    print(f"{risk_level}: {desc}\n")
