#!/usr/bin/env python3
"""Test real AI-powered features after model fix"""
import json
import urllib.request
import urllib.error

BASE = "http://localhost:8000"
API_KEY = "kd_dreaming007"
TOKEN = None

def req(method, path, body=None, auth=False):
    url = BASE + path
    headers = {"X-API-Key": API_KEY, "Content-Type": "application/json"}
    if auth and TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    data = json.dumps(body).encode() if body else None
    rq = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        resp = urllib.request.urlopen(rq, timeout=90)
        return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except:
            return e.code, {"raw": e.read().decode()[:300]}
    except Exception as e:
        return 0, {"error": str(e)}

# Login
print("=== Login ===")
s, r = req("POST", "/api/auth/login", {"username": "DebK", "password": "password123"})
TOKEN = r["access_token"]
print(f"✅ Logged in as {r['user']['display_name']}")

# Health check
print("\n=== Health ===")
s, r = req("GET", "/health")
print(f"Status: {r['status']}")
print(f"AI: {r['providers']['ai']['status']}")

# Test Feynman Session (AI-powered)
print("\n=== Feynman Session (AI) ===")
s, r = req("POST", "/api/feynman/session/start", {
    "topic": "photosynthesis",
    "difficulty_level": 5
}, auth=True)
print(f"[{s}] Session started: {json.dumps(r, ensure_ascii=False)[:200]}")
sid = r.get("session_id")

if sid:
    # Layer 1: Teach
    print("\n=== Layer 1: Teach ===")
    s, r = req("POST", f"/api/feynman/layer1/start?session_id={sid}", None, auth=True)
    print(f"[{s}] Layer1 start: {json.dumps(r, ensure_ascii=False)[:200]}")
    
    s, r = req("POST", "/api/feynman/layer1/teach", {
        "session_id": sid,
        "message": "Photosynthesis is the process by which plants convert sunlight, water and carbon dioxide into glucose and oxygen using chlorophyll in their leaves."
    }, auth=True)
    print(f"[{s}] Layer1 teach response: {json.dumps(r, ensure_ascii=False)[:300]}")

# Test Chat (AI-powered)
print("\n=== Chat with AI ===")
s, r = req("POST", "/api/chat/message", {
    "message": "Explain gravity simply for a 10 year old",
    "session_id": "test_chat"
}, auth=True)
print(f"[{s}] Chat: {json.dumps(r, ensure_ascii=False)[:300]}")

# Test Learning Session Start
print("\n=== Learning Session ===")
s, r = req("POST", "/api/learning/start", {
    "topic": "Solar System",
    "difficulty_level": 3,
    "duration_minutes": 5,
    "visual_style": "cartoon",
    "play_mode": "solo"
}, auth=True)
print(f"[{s}] Learning: {json.dumps(r, ensure_ascii=False)[:300]}")

print("\n=== Tests Complete ===")
