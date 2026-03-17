#!/usr/bin/env python3
"""Comprehensive test suite for FunLearn app at http://165.22.218.159"""
import json
import sys
import urllib.request
import urllib.error

BASE = "http://localhost:8000"
API_KEY = "kd_dreaming007"
TOKEN = None
RESULTS = []

def req(method, path, body=None, auth=False, expect_status=200):
    """Make HTTP request and return parsed JSON"""
    url = BASE + path
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    if auth and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    
    data = json.dumps(body).encode() if body else None
    rq = urllib.request.Request(url, data=data, headers=headers, method=method)
    
    try:
        resp = urllib.request.urlopen(rq, timeout=30)
        result = json.loads(resp.read().decode())
        return resp.status, result
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()
        try:
            result = json.loads(body_text)
        except:
            result = {"raw": body_text[:300]}
        return e.code, result
    except Exception as e:
        return 0, {"error": str(e)}

def test(name, method, path, body=None, auth=False, expect=200):
    status, result = req(method, path, body, auth)
    ok = status == expect
    icon = "✅" if ok else "❌"
    RESULTS.append((name, ok, status, result))
    summary = json.dumps(result, ensure_ascii=False)[:120] if isinstance(result, dict) else str(result)[:120]
    print(f"{icon} {name}: HTTP {status} — {summary}")
    return status, result

# ======================== TESTS ========================

print("=" * 60)
print("FUNLEARN APP TEST SUITE")
print("=" * 60)

# 1. ROOT
print("\n--- Basic Endpoints ---")
test("Root", "GET", "/")

# 2. HEALTH 
test("Health", "GET", "/health")

# 3. Docs
test("OpenAPI Docs", "GET", "/docs", expect=200)

# 4. LOGIN with correct credentials
print("\n--- Authentication ---")
s, r = test("Login DebK", "POST", "/api/auth/login", {"username": "DebK", "password": "password123"})
if s == 200:
    TOKEN = r.get("access_token")
    print(f"   Token: {TOKEN[:40]}...")
    print(f"   User: {r['user'].get('display_name')} | Role: {r['user'].get('role')} | XP: {r['user'].get('xp_points')} | Level: {r['user'].get('level')}")

# 5. LOGIN with wrong password
test("Login bad password", "POST", "/api/auth/login", {"username": "DebK", "password": "wrongpassword"}, expect=401)

# 6. LOGIN with non-existent user
test("Login bad user", "POST", "/api/auth/login", {"username": "nonexistent", "password": "password123"}, expect=401)

# 7. GET /api/auth/me
print("\n--- Authenticated Endpoints ---")
test("Get current user", "GET", "/api/auth/me", auth=True)

# 8. GET /api/users/profile
test("User profile", "GET", "/api/users/profile", auth=True)

# 9. GET sessions
test("List sessions", "GET", "/api/sessions/", auth=True)

# 10. Feynman topics
print("\n--- Feynman Engine ---")
test("Feynman topics", "GET", "/api/feynman/topics", auth=True)

# 11. Start Feynman session
s, r = test("Start Feynman session", "POST", "/api/feynman/session", 
    {"topic": "photosynthesis", "difficulty": 5}, auth=True)
feynman_session_id = r.get("session_id") if s == 200 else None
if feynman_session_id:
    print(f"   Session ID: {feynman_session_id}")

# 12. Feynman explain (if session started)
if feynman_session_id:
    test("Feynman explain", "POST", f"/api/feynman/session/{feynman_session_id}/explain",
        {"explanation": "Photosynthesis is how plants use sunlight to make food from CO2 and water"}, auth=True)

# 13. Learning endpoints
print("\n--- Learning/MCT ---")
test("Start learning session", "POST", "/api/learning/start", 
    {"topic": "Solar System", "difficulty": 3, "duration": 5, "style": "cartoon", "play_mode": "solo"}, auth=True)

# 14. Quiz
print("\n--- Quiz ---")
test("Get quiz questions", "GET", "/api/quiz/questions?topic=science&count=3", auth=True)

# 15. Chat
print("\n--- Chat ---")
test("Chat message", "POST", "/api/chat/message", 
    {"message": "What is photosynthesis?", "session_id": "test"}, auth=True)

# 16. Features/MCT
print("\n--- Features ---")
test("MCT diagnostics", "GET", "/api/features/mct/status", auth=True)

# 17. Admin endpoints  
print("\n--- Admin ---")
# Login as admin first
s, r = req("POST", "/api/auth/login", {"username": "admin", "password": "password123"})
if s == 200:
    admin_token = r.get("access_token")
    # temporarily use admin token
    old_token = TOKEN
    TOKEN = admin_token
    test("Admin dashboard", "GET", "/api/admin/dashboard", auth=True)
    test("Admin users list", "GET", "/api/admin/users", auth=True)
    TOKEN = old_token

# 18. Static assets  
print("\n--- Static Assets ---")
for path in ["/assets/index-DHln2E_O.js", "/assets/index-Tof18yjJ.css"]:
    try:
        rq = urllib.request.Request(f"http://localhost{path}")
        resp = urllib.request.urlopen(rq, timeout=10)
        size = len(resp.read())
        print(f"✅ Asset {path}: {size:,} bytes")
        RESULTS.append((f"Asset {path}", True, 200, {}))
    except Exception as e:
        print(f"❌ Asset {path}: {e}")
        RESULTS.append((f"Asset {path}", False, 0, {}))

# ======================== SUMMARY ========================
print("\n" + "=" * 60)
passed = sum(1 for _, ok, _, _ in RESULTS if ok)
failed = sum(1 for _, ok, _, _ in RESULTS if not ok)
total = len(RESULTS)
print(f"RESULTS: {passed}/{total} passed, {failed} failed")

if failed:
    print("\nFailed tests:")
    for name, ok, status, result in RESULTS:
        if not ok:
            print(f"  ❌ {name}: HTTP {status}")
print("=" * 60)
