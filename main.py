# main.py

def analyze_wallet(wallet_info, transactions, social_data):
    """
    Analyze wallet based on info, transactions, and social media scores.
    """
    score = 10

    # Example heuristics
    if wallet_info['final_balance'] > 10:
        score += 20
    if wallet_info['n_tx'] > 50:
        score += 30

    if any(tx['value'] > 1 for tx in transactions):
        score += 25

    score += min(social_data.get('trust_score', 0), 100) * 0.25

    return {
        "risk_score": 100 - score,
        "details": {
            "wallet": wallet_info,
            "transactions": transactions,
            "social_media": social_data
        }
    }
