# Realizer architecture

Realizer separates the browser gateway from AI inference.

- `app/` — responsive browser UI
- `backend/` — Python API bridge
- `workflows/` — ComfyUI API workflow files when used
- `tests/` — integration and regression tests
- GitHub Pages can serve the UI; it does not execute GPU inference.

The intended low-power-device flow is:

`Browser → Realizer backend/remote GPU → ComfyUI or hosted provider → video → Browser`
