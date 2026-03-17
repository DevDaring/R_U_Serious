#!/usr/bin/env python3
"""Comprehensive test suite v2 for FunLearn app — correct routes"""
import json
import urllib.request
import urllib.error

BASE = "http://localhost:8000"
API_KEY = "kd_dreaming007"
TOKEN = None
ADMIN_TOKEN = None
RESULTS = []

def req(method, path, body=None, auth=False, token_override=None):
    url = BASE + path
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    t = token_override or (TOKEN if auth else None)
    if t:
        headers["Authorization"] = f"Bearer {t}"
    data = json.dumps(body).encode() if body else None
    rq = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(rq, timeout=60)
        result = json.loads(resp.read().decode())
        return resp.status, result
    except urllib.error.HTTPError as e:
        try:
            result = json.loads(e.read().decode())
        except:
            result = {"raw": "non-json"}
        return e.code, result
    except Exception as e:
        return 0, {"error": str(e)}

def test(name, method, path, body=None, auth=False, expect=200, token_override=None):
    status, result = req(method, path, body, auth, token_override)
    ok = status == expect
    icon = "✅" if ok else "❌"
    RESULTS.append((name, ok, status))
    s = json.dumps(result, ensure_ascii=False)[:150] if isinstance(result, dict) else str(result)[:150]
    print(f"{icon} {name}: HTTP {status} — {s}")
    return status, result

print("=" * 60)
print("FUNLEARN APP — COMPREHENSIVE TEST v2")
print("=" * 60)

# ======= BASIC =======
print("\n🔹 BASIC ENDPOINTS")
test("Root", "GET", "/")
test("Health", "GET", "/health")

# ======= AUTH =======
print("\n🔹 AUTHENTICATION")
s, r = test("Login DebK (valid)", "POST", "/api/auth/login", {"username": "DebK", "password": "password123"})
if s == 200:
    TOKEN = r["access_token"]
    print(f"   ➤ User: {r['user']['display_name']} | role={r['user']['role']} | xp={r['user']['xp_points']} | level={r['user']['level']}")

test("Login wrong password", "POST", "/api/auth/login", {"username": "DebK", "password": "wrong"}, expect=401)
test("Login nonexistent user", "POST", "/api/auth/login", {"username": "ghost", "password": "password123"}, expect=401)

s, r = req("POST", "/api/auth/login", {"username": "admin", "password": "password123"})
if s == 200:
    ADMIN_TOKEN = r["access_token"]
    print(f"✅ Admin login: OK (role={r['user']['role']})")
else:
    print(f"❌ Admin login: HTTP {s}")

# ======= AUTH'D USER =======
print("\n🔹 USER ENDPOINTS")
test("GET /api/auth/me", "GET", "/api/auth/me", auth=True)
test("GET /api/users/profile", "GET", "/api/users/profile", auth=True)
test("GET /api/users/history", "GET", "/api/users/history", auth=True)
test("GET /api/sessions", "GET", "/api/sessions", auth=True)
test("GET /api/learning/sessions", "GET", "/api/learning/sessions", auth=True)
test("GET /api/learning/history", "GET", "/api/learning/history", auth=True)

# ======= LEARNING =======
print("\n🔹 LEARNING SESSION")
s, r = test("Start learning session", "POST", "/api/learning/start", {
    "topic": "Solar System",
    "difficulty_level": 3,
    "duration_minutes": 5,
    "visual_style": "cartoon",
    "play_mode": "solo"
}, auth=True)
learn_sid = None
if s in (200, 201):
    learn_sid = r.get("session_id") or r.get("session", {}).get("session_id")
    print(f"   ➤ Session: {learn_sid}")

# ======= FEYNMAN ENGINE =======
print("\n🔹 FEYNMAN ENGINE")
test("GET analogies", "GET", "/api/feynman/analogies", auth=True)

s, r = test("Start Feynman session", "POST", "/api/feynman/session/start", {
    "topic": "photosynthesis",
    "difficulty_level": 5
}, auth=True)
fey_sid = None
if s in (200, 201):
    fey_sid = r.get("session_id") or r.get("session", {}).get("session_id")
    print(f"   ➤ Feynman Session: {fey_sid}")

if fey_sid:
    test("GET Feynman session", "GET", f"/api/feynman/session/{fey_sid}", auth=True)
    test("Layer1 start", "POST", "/api/feynman/layer1/start", {"session_id": fey_sid}, auth=True)
    test("Layer1 teach", "POST", "/api/feynman/layer1/teach", {
        "session_id": fey_sid,
        "explanation": "Photosynthesis is how plants convert sunlight into energy using chlorophyll"
    }, auth=True)

# ======= STORY =======
print("\n🔹 STORY ENGINE")
test("Story health", "GET", "/api/story/health", auth=True)
test("Story generate", "POST", "/api/story/generate", {
    "topic": "gravity",
    "difficulty_level": 3,
    "style": "cartoon"
}, auth=True)

# ======= CHAT =======
print("\n🔹 CHAT")
test("Chat message", "POST", "/api/chat/message", {
    "message": "What is photosynthesis?",
    "session_id": "test123"
}, auth=True)

# ======= MCT / FEATURES =======
print("\n🔹 MCT (Mistake Correction)")
test("Start MCT session", "POST", "/api/features/mct/start", {
    "topic": "mathematics",
    "user_id": "USR002"
}, auth=True)
test("Mistake analyze", "POST", "/api/features/mistake/analyze", {
    "question": "What is 2+2?",
    "user_answer": "5",
    "correct_answer": "4"
}, auth=True)

# ======= QUIZ (needs a session) =======
print("\n🔹 QUIZ")
if learn_sid:
    test("Get MCQ questions", "GET", f"/api/quiz/session/{learn_sid}/mcq", auth=True)
    test("Get descriptive questions", "GET", f"/api/quiz/session/{learn_sid}/descriptive", auth=True)
else:
    print("⏭️  Skipped quiz tests (no learning session ID)")

# ======= ADMIN =======
print("\n🔹 ADMIN")
test("Admin user list", "GET", "/api/admin/users", auth=True, token_override=ADMIN_TOKEN)
test("Admin create tournament", "POST", "/api/admin/tournaments/create", {
    "name": "Test Tournament",
    "topic": "Science",
    "start_date": "2026-04-01",
    "end_date": "2026-04-07",
    "max_teams": 10
}, auth=True, token_override=ADMIN_TOKEN)

# ======= SUMMARY =======
print("\n" + "=" * 60)
passed = sum(1 for _, ok, _ in RESULTS if ok)
failed = sum(1 for _, ok, _ in RESULTS if not ok)
total = len(RESULTS)
print(f"RESULTS: {passed}/{total} passed, {failed} failed")

if failed:
    print("\n❌ FAILED TESTS:")
    for name, ok, status in RESULTS:
        if not ok:
            print(f"   • {name} → HTTP {status}")

print("=" * 60)
