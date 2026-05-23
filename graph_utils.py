import matplotlib.pyplot as plt
from collections import Counter

# Wallet summary bar chart
def plot_wallet_summary(wallet_info):
    received = wallet_info.get('total_received', 0)
    sent = wallet_info.get('total_sent', 0)
    final = wallet_info.get('final_balance', 0)
    fig, ax = plt.subplots()
    ax.bar(['Received', 'Sent', 'Balance'], [received, sent, final], color=['green','red','blue'])
    ax.set_title('Wallet Summary')
    ax.set_ylabel('BTC Amount')
    return fig

# Transaction amount bar chart
def plot_transaction_amounts(transactions):
    types = [tx.get('type', 'BTC') for tx in transactions]
    amounts = [tx.get('amount', 0) for tx in transactions]
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(range(len(amounts)), amounts, color='purple')
    ax.set_title('Transaction Amounts')
    ax.set_xlabel('Transaction #')
    ax.set_ylabel('Amount')
    ax.set_xticks(range(len(amounts)))
    ax.set_xticklabels(types, rotation=45)
    return fig
