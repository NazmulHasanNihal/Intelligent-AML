import time
import json
import random
import urllib.request
import urllib.error

# Simulate a network of accounts for our synthetic data
ACCOUNTS = [f"ACC_{str(i).zfill(5)}" for i in range(1, 1001)]
HIGH_RISK_ACCOUNTS = ACCOUNTS[:10]  # First 10 are designated "high risk"

def generate_transaction():
    """
    Generates a realistic transaction.
    Most are normal, but injects occasional AML suspicious patterns.
    """
    is_suspicious = random.random() < 0.15 # 15% chance of anomalous pattern
    
    if is_suspicious:
        pattern = random.choice(["structuring", "large_transfer", "high_risk_activity"])
        if pattern == "structuring":
            # Structuring / Smurfing: Amounts just below the $10k reporting threshold
            amount = random.uniform(9500.0, 9999.0)
            src = random.choice(ACCOUNTS)
            dst = random.choice(ACCOUNTS)
        elif pattern == "large_transfer":
            # Unusually large transfer
            amount = random.uniform(50000.0, 1000000.0)
            src = random.choice(ACCOUNTS)
            dst = random.choice(ACCOUNTS)
        else:
            # Activity involving a known high-risk account
            amount = random.uniform(500.0, 5000.0)
            src = random.choice(HIGH_RISK_ACCOUNTS)
            dst = random.choice(ACCOUNTS)
    else:
        # Normal, everyday transactions (e.g. coffee, rent, groceries, salary)
        amount = random.lognormvariate(4.0, 1.5)  # Log-normal distribution typical for payments
        # Clamp normal transactions between 1 and 10000 for realism
        amount = max(1.0, min(amount, 10000.0))
        src = random.choice(ACCOUNTS)
        dst = random.choice(ACCOUNTS)
        
    # Prevent self-transfer
    while src == dst:
        dst = random.choice(ACCOUNTS)
        
    return {
        "transaction_id": f"tx_{int(time.time() * 1000)}_{random.randint(1000, 9999)}",
        "source_account": src,
        "target_account": dst,
        "amount": round(amount, 2),
        "timestamp": time.time(),
        "currency": "USD",
        "is_flagged": False # System will evaluate this later
    }

def send_transaction(tx):
    url = "http://localhost:8000/transaction"
    headers = {'Content-Type': 'application/json'}
    data = json.dumps(tx).encode('utf-8')
    req = urllib.request.Request(url, data=data, headers=headers, method='POST')
    
    try:
        response = urllib.request.urlopen(req)
        if response.status == 200:
            print(f"Sent: {tx['transaction_id']} | Amount: ${tx['amount']:,.2f} | {tx['source_account']} -> {tx['target_account']}")
        else:
            print(f"Failed to send {tx['transaction_id']} - HTTP {response.status}")
    except urllib.error.URLError as e:
        print(f"Connection failed (is the API running?): {e}")

if __name__ == "__main__":
    print("Starting Realistic Mock Data Generator...")
    print("Simulating live transactions with built-in AML patterns (structuring, large transfers)...")
    
    # Wait a few seconds to let FastAPI spin up
    time.sleep(5)
    
    try:
        while True:
            tx = generate_transaction()
            send_transaction(tx)
            # Sleep for a random interval to simulate bursty traffic
            time.sleep(random.uniform(0.1, 1.5))
    except KeyboardInterrupt:
        print("\nStopping generator...")
