#!/bin/bash
set -e
API_KEY="kd_dreaming007"
BASE="http://localhost:8000"

echo "=== Login ==="
LOGIN=$(curl -s -X POST "$BASE/api/auth/login" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"username":"DebK","password":"password123"}')
echo "$LOGIN"
TOKEN=$(echo "$LOGIN" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("token",""))')
echo "Token length: ${#TOKEN}"

echo ""
echo "=== Start Feynman Session ==="
SESSION=$(curl -s -X POST "$BASE/api/feynman/session/start" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"user_id":"user_DebK","topic":"Photosynthesis","difficulty_level":5}')
echo "$SESSION" | python3 -c 'import sys,json; d=json.load(sys.stdin); print("Session ID:", d.get("session_id",""))'
SESSION_ID=$(echo "$SESSION" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("session_id",""))')

echo ""
echo "=== Test Feynman Layer 1 Teach (with illustration) ==="
TEACH=$(curl -s -X POST "$BASE/api/feynman/layer1/teach" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -H "Authorization: Bearer $TOKEN" \
  -d "{\"session_id\":\"$SESSION_ID\",\"user_id\":\"user_DebK\",\"topic\":\"Photosynthesis\",\"message\":\"How does photosynthesis work?\",\"difficulty_level\":5}")
echo "$TEACH" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("Keys:", list(d.keys()))
i = d.get("illustration")
print("HAS_ILLUSTRATION:", i is not None)
if i and isinstance(i, dict):
    print("  Title:", i.get("title", "N/A"))
    print("  Visual type:", i.get("visual_type", "N/A"))
    print("  Elements:", len(i.get("elements", [])))
elif "detail" in d:
    print("  ERROR:", d["detail"])
'

echo ""
echo "=== Frontend check ==="
HTTP=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:80/)
echo "Frontend HTTP: $HTTP"

echo ""
echo "=== Done ==="
