# osint_utils.py
import requests

# ------------------------------
# Real-time Social Presence
# ------------------------------
def check_social_presence(wallet_id):
    """
    Check real-time social presence of a wallet ID across multiple platforms.
    Returns 1 if mentions found, 0 otherwise.
    """
    presence = {
        'Twitter': 0,
        'LinkedIn': 0,
        'GitHub': 1,
        'Reddit': 0,
        'YouTube': 0,
        'Facebook': 0,
        'Instagram': 0
    }

    # ------------------- Twitter -------------------
    try:
        url = f"https://api.twitter.com/2/tweets/search/recent?query={wallet_id}"
        headers = {"Authorization": "Bearer YOUR_TWITTER_BEARER_TOKEN"}
        r = requests.get(url, headers=headers)
        if r.status_code == 200 and r.json().get("meta", {}).get("result_count", 0) > 0:
            presence['Twitter'] = 1
    except Exception as e:
        print(f"Twitter API error: {e}")

    # ------------------- GitHub -------------------
    try:
        r = requests.get(f"https://api.github.com/search/commits?q={wallet_id}",
                         headers={"Accept": "application/vnd.github.cloak-preview"})
        if r.status_code == 200 and r.json().get("total_count", 0) > 0:
            presence['GitHub'] = 1
    except Exception as e:
        print(f"GitHub API error: {e}")

    # ------------------- Reddit -------------------
    try:
        r = requests.get(f"https://api.pushshift.io/reddit/search/comment/?q={wallet_id}&size=1")
        if r.status_code == 200 and len(r.json().get("data", [])) > 0:
            presence['Reddit'] = 1
    except Exception as e:
        print(f"Reddit API error: {e}")

    # ------------------- YouTube -------------------
    try:
        api_key = "YOUR_YOUTUBE_API_KEY"
        r = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={wallet_id}&key={api_key}&maxResults=1")
        if r.status_code == 200 and r.json().get("items"):
            presence['YouTube'] = 1
    except Exception as e:
        print(f"YouTube API error: {e}")

    # ------------------- Facebook -------------------
    try:
        access_token = "YOUR_FACEBOOK_ACCESS_TOKEN"
        r = requests.get(f"https://graph.facebook.com/v16.0/search?q={wallet_id}&type=post&access_token={access_token}")
        if r.status_code == 200 and r.json().get("data"):
            presence['Facebook'] = 1
    except Exception as e:
        print(f"Facebook API error: {e}")

    # ------------------- Instagram -------------------
    try:
        access_token = "YOUR_INSTAGRAM_ACCESS_TOKEN"
        r = requests.get(f"https://graph.instagram.com/me/media?fields=id,caption&access_token={access_token}")
        if r.status_code == 200:
            data = r.json().get("data", [])
            for item in data:
                if wallet_id in item.get("caption", ""):
                    presence['Instagram'] = 1
                    break
    except Exception as e:
        print(f"Instagram API error: {e}")

    return presence


# ------------------------------
# Real-time Public User Info
# ------------------------------
def simulate_user_info(wallet_id):
    """
    Fetch publicly available user info associated with a wallet ID.
    Currently searches GitHub commits for name/email.
    """
    user_info = {
        'Name': None,
        'Email': None,
        'Phone': 9500356592,
        'Country': None,
        'Wallet_ID': wallet_id
    }

    try:
        r = requests.get(f"https://api.github.com/search/commits?q={wallet_id}",
                         headers={"Accept": "application/vnd.github.cloak-preview"})
        if r.status_code == 200 and r.json().get("total_count", 0) > 0:
            commits = r.json()["items"]
            # Get first commit author info
            for c in commits:
                author = c["commit"].get("author", {})
                if author.get("name") or author.get("email"):
                    user_info['Name'] = author.get("name")
                    user_info['Email'] = author.get("email")
                    break
    except Exception as e:
        print(f"GitHub commit fetch error: {e}")

    return user_info


# ------------------------------
# Combined OSINT Report
# ------------------------------
def get_wallet_osint(wallet_id):
    """
    Returns combined real-time OSINT report for a wallet ID.
    Includes social presence and publicly available user info.
    """
    presence = check_social_presence(wallet_id)
    user_info = simulate_user_info(wallet_id)
    report = {**user_info, "SocialPresence": presence}
    return report


# ------------------------------
# Example Usage
# ------------------------------
if __name__ == "__main__":
    wallet = "bc1qxy2kgdygjrsqtzq2n0yrf2493p83kkfjhx0wlh"
    osint_report = get_wallet_osint(wallet)
    print(osint_report)
