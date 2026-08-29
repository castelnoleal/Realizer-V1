# Realizer tests

The backend can be syntax-checked with:

```bash
python -m py_compile backend/server.py
```

For integration testing, run the backend and query `/api/health`. Full AI inference testing must be performed against the target ComfyUI/model installation because GitHub Pages and this repository do not provide GPU inference.
