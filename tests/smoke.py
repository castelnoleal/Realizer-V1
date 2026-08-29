import urllib.request, json

base='http://127.0.0.1:8000'
with urllib.request.urlopen(base+'/api/health', timeout=5) as r:
    data=json.loads(r.read().decode())
assert data.get('ok') is True
print('Realizer backend smoke test: PASS')
