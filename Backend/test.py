import requests


BASE_URL = "http://localhost:5000"

# Test 1 - math questions
print("=== sending messages ===")

messages = [
    {"student": "alice", "message": "how do i solve an integral of x^2"},
    {"student": "alice", "message": "what is the maximum value of x^2 - 4x + 3"},
    {"student": "bob", "message": "prove by induction that 1+2+...+n = n(n+1)/2"},
    {"student": "bob", "message": "what is sin(90)"},
    {"student": "alice", "message": "what is the capital of France"},  # should be אחר
    {"student": "bob", "message": "find the sum of the geometric series"},
]

for msg in messages:
    r = requests.post(f"{BASE_URL}/send_message", json=msg)
    print(f"{msg['message'][:40]:<40} → {r.json()['classification']}")

# Test 2 - full message log
print("\n=== all messages ===")
r = requests.get(f"{BASE_URL}/get_messages")
for msg in r.json():
    print(f"[{msg['student']}] {msg['subject']} — {msg['message'][:40]}")

# Test 3 - stats (אחר should not appear here)
print("\n=== stats ===")
r = requests.get(f"{BASE_URL}/get_stats")
for stat in r.json():
    print(f"{stat['subject']}: {stat['count']} questions")