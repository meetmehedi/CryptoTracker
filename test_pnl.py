import requests
import json

BASE_URL = "http://127.0.0.1:5001"
SESSION = requests.Session()

def test_pnl_flow():
    # Register (ignore if exists)
    SESSION.post(f"{BASE_URL}/register", json={"name": "Test", "email": "test@example.com", "password": "password123"})

    # Login
    res = SESSION.post(f"{BASE_URL}/api/login", json={"email": "test@example.com", "password": "password123"})
    print(f"Login Status: {res.status_code}")
    if res.status_code != 200:
        print("Login Failed:", res.text)
        return
    
    # Get Coins
    coins = SESSION.get(f"{BASE_URL}/coins").json()
    coin_id = coins[0][0] # First coin
    
    # 1. Buy 10 at $100
    print("Buying 10 @ $100...")
    SESSION.post(f"{BASE_URL}/transaction", json={
        "coin_id": coin_id, "type": "buy", "quantity": 10.0, "price_at_time": 100.0
    })
    
    # 2. Buy 10 at $200
    print("Buying 10 @ $200...")
    SESSION.post(f"{BASE_URL}/transaction", json={
        "coin_id": coin_id, "type": "buy", "quantity": 10.0, "price_at_time": 200.0
    })
    
    # Expected Avg: (1000 + 2000) / 20 = $150
    
    # Check Holdings
    holdings = SESSION.get(f"{BASE_URL}/get_holdings").json()
    print("Holdings:", holdings)
    
    # Find our coin
    for h in holdings:
        # row: symbol, name, quantity, current_price, avg_buy_price
        # Note: quantity might be aggregated from other tests, specifically integration test might have added 5 previously.
        # But avg calculation should hold for the *new* transactions if logic is correct.
        # Let's just print to verify visually for now.
        if h[4]: # avg_buy_price
            print(f"Symbol: {h[0]}, Qty: {h[2]}, Avg: {h[4]}")

if __name__ == "__main__":
    test_pnl_flow()
