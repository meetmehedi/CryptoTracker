import requests
import json

BASE_URL = "http://127.0.0.1:5001"
SESSION = requests.Session()

def test_register():
    print("Testing Register...")
    res = SESSION.post(f"{BASE_URL}/register", json={
        "name": "Integration Test User",
        "email": "test@example.com",
        "password": "password123"
    })
    # might fail if already exists, that's fine
    print(f"Register Status: {res.status_code}")

def test_login():
    print("Testing Login...")
    res = SESSION.post(f"{BASE_URL}/api/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    print(f"Login Status: {res.status_code}")
    print(f"Login Response: {res.text}")
    assert res.status_code == 200

def test_dashboard_access():
    print("Testing Dashboard Access (Session Check)...")
    res = SESSION.get(f"{BASE_URL}/")
    print(f"Dashboard Title in response: {'Crypto Portfolio' in res.text}")
    # Should NOT be login page
    assert "Login - Crypto Portfolio" not in res.text

def test_transaction():
    print("Testing Transaction...")
    # Get Coin first
    res = SESSION.get(f"{BASE_URL}/coins")
    coins = res.json()
    coin_id = coins[0][0] # First coin ID
    
    res = SESSION.post(f"{BASE_URL}/transaction", json={
        "coin_id": coin_id,
        "type": "buy",
        "quantity": 5.0,
        "price_at_time": 1234.56
    })
    print(f"Transaction Status: {res.status_code}")
    assert res.status_code == 201

def test_holdings():
    print("Testing Holdings...")
    res = SESSION.get(f"{BASE_URL}/get_holdings")
    print(f"Holdings: {res.json()}")
    assert len(res.json()) > 0

if __name__ == "__main__":
    try:
        test_register()
        test_login()
        test_dashboard_access()
        test_transaction()
        test_holdings()
        print("ALL TESTS PASSED")
    except Exception as e:
        print(f"TEST FAILED: {e}")
