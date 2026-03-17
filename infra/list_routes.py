import sys, json, urllib.request
r = urllib.request.urlopen("http://localhost:8000/openapi.json")
d = json.loads(r.read().decode())
paths = sorted(d.get("paths", {}).keys())
for p in paths:
    methods = list(d["paths"][p].keys())
    print(f"{methods[0].upper():6s} {p}")
