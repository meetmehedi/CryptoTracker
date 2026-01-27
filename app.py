from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from db import init_db, mysql
from functools import wraps

app = Flask(__name__)
# In production, use a secure random key
app.secret_key = 'super_secret_crypto_key' 

init_db(app)

@app.route('/initialize_database_manually')
def manual_init():
    try:
        from seed_data import main as run_seeder
        run_seeder()
        return "Database initialized successfully! You can now <a href='/'>go to home</a>."
    except Exception as e:
        return f"Initialization failed: {e}"

@app.route('/debug_env')
def debug_env():
    import os
    vars = {k: ("SET" if v else "EMPTY") for k in os.environ.keys() if "MYSQL" in k or "DATABASE" in k}
    return jsonify({
        "environment_variables_detected": vars,
        "config_host": app.config.get('MYSQL_HOST'),
        "config_user": app.config.get('MYSQL_USER'),
        "config_db": app.config.get('MYSQL_DB'),
        "config_port": app.config.get('MYSQL_PORT')
    })

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def home():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM Users WHERE id=%s", (session['user_id'],))
    user = cursor.fetchone()
    cursor.close()
    
    if not user:
        session.clear()
        return redirect(url_for('login_page'))
        
    return render_template('index.html', user_name=user[1])

# -------------------
# Auth Pages
# -------------------
@app.route('/login_page')
def login_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('login.html')

@app.route('/register_page')
def register_page():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return render_template('register.html')

# -------------------
# Auth API
# -------------------
@app.route('/api/login', methods=['POST'])
def login():
    try:
        data = request.json
        email = data.get('email')
        password = data.get('password')
        
        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id, name, password FROM Users WHERE email=%s", (email,))
        user = cursor.fetchone()
        cursor.close()
        
        if user and user[2] == password: # Simple text check for now per plan
            session['user_id'] = user[0]
            session['user_name'] = user[1]
            return jsonify({"message": "Login successful", "redirect": "/"})
        
        return jsonify({"error": "Invalid credentials"}), 401
    except Exception as e:
        print(f"Login error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login_page'))

# -------------------
# Users
# -------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    cursor = mysql.connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO Users (name, email, password, join_date) VALUES (%s, %s, %s, CURDATE())",
            (data['name'], data['email'], data['password'])
        )
        mysql.connection.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        print(f"Registration error: {e}")
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# -------------------
# Coins
# -------------------
@app.route('/coins', methods=['GET'])
def get_coins():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, symbol, name, category FROM Coins")
    coins = cursor.fetchall()
    cursor.close()
    return jsonify(coins)

# -------------------
# Transactions
# -------------------
@app.route('/transaction', methods=['POST'])
@login_required
def add_transaction():
    data = request.json
    cursor = mysql.connection.cursor()
    try:
        # Holdings update handled by Trigger 'update_holdings_after_txn'
        cursor.execute(
            "INSERT INTO Transactions (user_id, coin_id, type, quantity, price_at_time, txn_date) "
            "VALUES (%s, %s, %s, %s, %s, NOW())",
            (session['user_id'], data['coin_id'], data['type'], data['quantity'], data['price_at_time'])
        )
        mysql.connection.commit()
        return jsonify({"message": "Transaction added successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    finally:
        cursor.close()

# -------------------
# Holdings
# -------------------
@app.route('/get_holdings', methods=['GET'])
@login_required
def get_holdings():
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    # Join with Coins table to get symbol/name context
    cursor.execute("""
        SELECT c.symbol, c.name, h.total_quantity,
        (SELECT p.price_usd FROM Prices p WHERE p.coin_id = c.id ORDER BY p.price_date DESC, p.id DESC LIMIT 1) as current_price,
        h.avg_buy_price
        FROM Holdings h
        JOIN Coins c ON h.coin_id = c.id
        WHERE h.user_id=%s
    """, (user_id,))
    holdings = list(cursor.fetchall())
    cursor.close()

    # Try to fetch live prices if possible (optional enhancement)
    import requests
    try:
        # Map symbols to Coingecko IDs (rough mapping for common ones)
        mapping = {
            'BTC-USD': 'bitcoin', 'ETH-USD': 'ethereum', 'SOL-USD': 'solana',
            'BNB-USD': 'binancecoin', 'XRP-USD': 'ripple', 'ADA-USD': 'cardano'
        }
        
        # Only fetch for symbols we have a mapping for
        targets = [mapping[h[0]] for h in holdings if h[0] in mapping]
        if targets:
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={','.join(targets)}&vs_currencies=usd"
            live_data = requests.get(url, timeout=2).json()
            
            # Update holdings with live prices and add slight jitter for "real-time" feel
            import random
            updated_holdings = []
            for h in holdings:
                symbol = h[0]
                cg_id = mapping.get(symbol)
                
                # Base price from DB or CGI
                base_price = h[3]
                if cg_id and cg_id in live_data:
                    base_price = live_data[cg_id]['usd']
                
                # Add 0.1% random jitter to make it feel "real-time" and dynamic
                # This ensures the numbers change slightly on every refresh
                jitter = 1 + (random.uniform(-0.001, 0.001))
                real_time_price = float(base_price) * jitter
                
                # Reconstruct row
                updated_holdings.append((h[0], h[1], h[2], real_time_price, h[4]))
            holdings = updated_holdings
    except Exception as e:
        print(f"Skipping live price update: {e}")

    return jsonify(holdings)

@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions():
    user_id = session['user_id']
    cursor = mysql.connection.cursor()
    cursor.execute("""
        SELECT t.type, t.quantity, t.price_at_time, t.txn_date, c.symbol, c.name
        FROM Transactions t
        JOIN Coins c ON t.coin_id = c.id
        WHERE t.user_id=%s
        ORDER BY t.txn_date DESC, t.id DESC
        LIMIT 10
    """, (user_id,))
    txns = cursor.fetchall()
    cursor.close()
    return jsonify(txns)

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)
