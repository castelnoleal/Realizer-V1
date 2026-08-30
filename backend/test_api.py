"""FastAPI smoke tests that do not require ComfyUI."""
from fastapi.testclient import TestClient
from backend.server import app

client=TestClient(app)

def test_health():
    r=client.get('/api/health')
    assert r.status_code==200
    assert r.json()['ok'] is True
    assert r.json()['image_to_video_endpoint'] is True

def test_setup_scan_without_comfyui():
    r=client.get('/api/setup/scan')
    assert r.status_code==200
    d=r.json()
    assert d['backend'] is True
    assert 'comfyui' in d and 'models' in d

def test_generate_without_comfyui_returns_clear_error():
    r=client.post('/api/generate',json={'prompt':'browser smoke test'})
    assert r.status_code in (503,502)

def test_image_endpoint_rejects_missing_image():
    r=client.post('/api/generate/image-to-video',data={'prompt':'animate this'})
    assert r.status_code in (400,422)
