# Realizer backend

Run from this directory:

```bash
python -m pip install -r requirements.txt
python -m uvicorn server:app --host 0.0.0.0 --port 8000
```

The backend is the bridge between the lightweight browser gateway and the actual video-generation engine/provider. Keep secrets and provider credentials server-side.
