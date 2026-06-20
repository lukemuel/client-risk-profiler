"""
Stage 1: Client Risk Profile Scoring
----------------------------------------
Goal: take basic client answers and convert them into
a risk score, then bucket into Conservative/Moderate/Aggressive.
"""

# -----------------------------
# 1. Define the scoring questions
# -----------------------------
# Each answer maps to points. More points = higher risk tolerance.
# This mirrors a real broker intake questionnaire (simplified).

def score_age(age):
    """Younger clients can generally take more risk (longer time to recover from losses)."""
    if age < 35:
        return 25
    elif age < 50:
        return 18
    elif age < 65:
        return 10
    else:
        return 4

def score_time_horizon(years_until_needed):
    """Longer time horizon = more risk capacity."""
    if years_until_needed >= 20:
        return 25
    elif years_until_needed >= 10:
        return 18
    elif years_until_needed >= 5:
        return 10
    else:
        return 4

def score_income_stability(stability):
    """stability: 'stable', 'somewhat_stable', 'unstable'"""
    mapping = {"stable": 20, "somewhat_stable": 12, "unstable": 5}
    return mapping.get(stability, 10)

def score_loss_tolerance(reaction):
    """
    reaction: how would the client react to a 20% portfolio drop?
    'buy_more', 'hold', 'sell_some', 'sell_all'
    """
    mapping = {
        "buy_more": 30,
        "hold": 22,
        "sell_some": 10,
        "sell_all": 0,
    }
    return mapping.get(reaction, 15)

# -----------------------------
# 2. Combine into a total risk score
# -----------------------------
def calculate_risk_score(age, years_until_needed, income_stability, loss_reaction):
    score = (
        score_age(age)
        + score_time_horizon(years_until_needed)
        + score_income_stability(income_stability)
        + score_loss_tolerance(loss_reaction)
    )
    return score

# -----------------------------
# 3. Map score to risk bucket
# -----------------------------
def get_risk_bucket(score):
    if score >= 70:
        return "Aggressive"
    elif score >= 45:
        return "Moderate"
    else:
        return "Conservative"

# -----------------------------
# 4. Test with sample clients
# -----------------------------
sample_clients = [
    {
        "name": "Client A (young, long horizon, stable, calm under pressure)",
        "age": 28,
        "years_until_needed": 30,
        "income_stability": "stable",
        "loss_reaction": "buy_more",
    },
    {
        "name": "Client B (mid-career, moderate horizon)",
        "age": 45,
        "years_until_needed": 15,
        "income_stability": "somewhat_stable",
        "loss_reaction": "hold",
    },
    {
        "name": "Client C (near retirement, low risk tolerance)",
        "age": 62,
        "years_until_needed": 3,
        "income_stability": "stable",
        "loss_reaction": "sell_some",
    },
]

print("=== CLIENT RISK PROFILE RESULTS ===\n")
for client in sample_clients:
    score = calculate_risk_score(
        client["age"],
        client["years_until_needed"],
        client["income_stability"],
        client["loss_reaction"],
    )
    bucket = get_risk_bucket(score)
    print(f"{client['name']}")
    print(f"  Risk Score: {score}/100")
    print(f"  Risk Bucket: {bucket}\n")
