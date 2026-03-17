#!/bin/bash
set -e

echo "=== Testing Health ==="
curl -s http://localhost:8000/health | python3 -m json.tool

echo ""
echo "=== Testing Login ==="
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"username":"DebK","password":"password123"}' | python3 -c 'import sys,json; print(json.load(sys.stdin).get("token",""))')
echo "TOKEN length: ${#TOKEN} chars"
echo "TOKEN: ${TOKEN:0:20}..."

echo ""
echo "=== Testing Feynman Layer 1 (with illustration) ==="
RESPONSE=$(curl -s -X POST http://localhost:8000/api/feynman/layer1/teach \
  -H 'Content-Type: application/json' \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"session_id":"test-illust-005","user_id":"user_DebK","topic":"Photosynthesis","message":"How does photosynthesis work?","difficulty_level":5}')

echo "$RESPONSE" | python3 -c '
import sys, json
d = json.load(sys.stdin)
print("Response Keys:", list(d.keys()))
i = d.get("illustration")
print("HAS_ILLUSTRATION:", i is not None)
if i:
    print("  Title:", i.get("title", "N/A"))
    print("  Visual type:", i.get("visual_type", "N/A"))
    print("  Elements count:", len(i.get("elements", [])))
    print("  Key insight:", str(i.get("key_insight", "N/A"))[:80])
else:
    print("  (illustration is None or missing)")
if "detail" in d:
    print("  ERROR detail:", d["detail"])
'

echo ""
echo "=== Testing Frontend ==="
HTTP_CODE=$(curl -s -o /dev/null -w '%{http_code}' http://localhost:80/)
echo "Frontend HTTP: $HTTP_CODE"

echo ""
echo "=== Backend logs (last 10 lines) ==="
journalctl -u funlearn-backend --no-pager -n 10

echo ""
echo "=== All tests done ==="
