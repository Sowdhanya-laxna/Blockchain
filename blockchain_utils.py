import requests
from datetime import datetime

# 🔹 Fetch wallet transactions in real time
def fetch_wallet_transactions(wallet_id):
    url = f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet_id}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()

        txrefs = data.get("txrefs", []) + data.get("unconfirmed_txrefs", [])
        txrefs = sorted(txrefs, key=lambda x: x.get("confirmed", ""), reverse=True)[:10]

        transactions = []
        for tx in txrefs:
            # Determine transaction direction and counterparty
            if tx["tx_output_n"] >= 0:
                direction = "Received"
                counterparty = tx.get("tx_input_n", "Unknown")  # Could refine later
            else:
                direction = "Sent"
                counterparty = tx.get("tx_output_n", "Unknown")  # Could refine later

            # Format timestamp
            timestamp = tx.get("confirmed")
            if timestamp:
                timestamp = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%Y-%m-%d")
            else:
                timestamp = "Pending"

            transactions.append({
                "date": timestamp,
                "from": tx.get("addresses", [wallet_id])[0] if direction == "Received" else wallet_id,
                "to": wallet_id if direction == "Received" else tx.get("addresses", ["Unknown"])[0],
                "amount": tx["value"] / 1e8,  # satoshis → BTC
                "type": "BTC"  # You can label differently if needed
            })

        # Wallet summary
        summary_url = f"https://api.blockcypher.com/v1/btc/main/addrs/{wallet_id}/balance"
        summary_resp = requests.get(summary_url)
        summary_resp.raise_for_status()
        summary_data = summary_resp.json()

        return {
            'wallet_id': wallet_id,
            'total_received': summary_data.get("total_received", 0) / 1e8,
            'total_sent': summary_data.get("total_sent", 0) / 1e8,
            'final_balance': summary_data.get("final_balance", 0) / 1e8,
            'transactions': transactions
        }

    except Exception as e:
        print("Error fetching wallet data:", e)
        return {}

# 🔹 Example usage
if __name__ == "__main__":
    wallet = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    data = fetch_wallet_transactions(wallet)
    print(data)
