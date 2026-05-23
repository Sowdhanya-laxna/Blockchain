from flask import Flask, render_template, request, redirect, url_for, session, flash
from blockchain_utils import fetch_wallet_transactions
from osint_utils import check_social_presence, simulate_user_info
from graph_utils import plot_wallet_summary, plot_transaction_amounts
import io, base64
from functools import wraps

app = Flask(__name__)
app.secret_key = 'secretkey123'
app.permanent_session_lifetime = 1800

def get_image_data_url(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches='tight')
    buf.seek(0)
    img_bytes = base64.b64encode(buf.read()).decode("utf-8")
    return f"data:image/png;base64,{img_bytes}"

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Please login as admin first.', 'warning')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

ADMIN_USERNAME = 'admin'
ADMIN_PASSWORD = 'admin123'

# ----------------- HOME PAGE -----------------
@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

# ----------------- ADMIN LOGIN -----------------
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['admin_logged_in'] = True
            flash('Admin logged in successfully.', 'success')
            return redirect(url_for('index'))  # <-- updated
        else:
            flash('Invalid credentials.', 'danger')
    return render_template('admin_login.html')


# ----------------- DASHBOARD / WALLET PAGE -----------------
@app.route('/index', methods=['GET', 'POST'])
@admin_required
def index():
    if request.method == 'POST':
        wallet_id = request.form.get('wallet_id', '').strip()
        if wallet_id:
            session['wallet_id'] = wallet_id
        else:
            flash('Wallet ID is required.', 'danger')
            return redirect(url_for('index'))

    if 'wallet_id' not in session:
        flash('Please enter a wallet ID.', 'warning')
        return render_template('index.html')

    wallet_info = fetch_wallet_transactions(session['wallet_id'])
    wallet_summary_image = get_image_data_url(plot_wallet_summary(wallet_info))
    tx_image = get_image_data_url(plot_transaction_amounts(wallet_info.get('transactions', [])))
    social_data = check_social_presence(session['wallet_id'])
    user_info = simulate_user_info(session['wallet_id'])

    return render_template('dashboard.html',
                           wallet_summary_image=wallet_summary_image,
                           tx_image=tx_image,
                           social_data=social_data,
                           user_info=user_info)

# ----------------- OTHER PAGES -----------------
@app.route('/summary')
@admin_required
def summary():
    if 'wallet_id' not in session:
        flash('Please enter a wallet ID.', 'warning')
        return redirect(url_for('index'))
    wallet_info = fetch_wallet_transactions(session['wallet_id'])
    wallet_summary_image = get_image_data_url(plot_wallet_summary(wallet_info))
    return render_template('summary.html', wallet_info=wallet_info,
                           wallet_summary_image=wallet_summary_image)

@app.route('/transactions')
@admin_required
def transactions():
    if 'wallet_id' not in session:
        flash('Please enter a wallet ID.', 'warning')
        return redirect(url_for('index'))
    wallet_info = fetch_wallet_transactions(session['wallet_id'])
    tx_image = get_image_data_url(plot_transaction_amounts(wallet_info.get('transactions', [])))
    return render_template('transactions.html', wallet_info=wallet_info, tx_image=tx_image)

@app.route('/social')
@admin_required
def social():
    if 'wallet_id' not in session:
        flash('Please enter a wallet ID.', 'warning')
        return redirect(url_for('index'))
    social_data = check_social_presence(session['wallet_id'])
    return render_template('social.html', social_data=social_data)

@app.route('/user')
@admin_required
def user():
    if 'wallet_id' not in session:
        flash('Please enter a wallet ID.', 'warning')
        return redirect(url_for('index'))
    user_info = simulate_user_info(session['wallet_id'])
    return render_template('user_info.html', user_info=user_info)

# ----------------- LOGOUT -----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('admin_login'))

# ----------------- ROOT REDIRECT -----------------
@app.route('/')
def root():
    return redirect(url_for('home'))

# ----------------- RUN APP -----------------
import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
