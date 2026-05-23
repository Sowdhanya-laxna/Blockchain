def analyze_wallet(wallet_info, transactions):
    risk_score = 10

    # Simple heuristic rules (customize these as needed)
    if len(transactions) > 100:
        risk_score += 30
    if wallet_info.get("is_blacklisted", False):
        risk_score += 50
    if wallet_info.get("activity", "") == "suspicious":
        risk_score += 20

    return {
        "wallet_info": wallet_info,
        "transactions": transactions,
        "risk_score": risk_score
    }
