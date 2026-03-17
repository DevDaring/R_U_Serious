import json, urllib.request
data = json.dumps({"session_id": "e998e5da-1542-4beb-a3b1-0583b485c6f4", "analogy_text": "Gravity is like a rubber sheet", "phase": "create"}).encode()
req = urllib.request.Request("http://localhost:8000/api/feynman/layer4/submit", data=data, headers={"Content-Type": "application/json"})
try:
    resp = urllib.request.urlopen(req, timeout=60)
    print(resp.read().decode())
except Exception as e:
    print(f"Error: {e}")
    if hasattr(e, "read"):
        print(e.read().decode())
