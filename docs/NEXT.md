# Realizer V1 current state

Implemented:
- Browser image upload validation and preview module
- Image-to-video backend boundary
- Provider registry
- ComfyUI HTTP adapter
- Generic remote GPU HTTP adapter
- Job store and normalized generation contracts
- Automated tests and CI

Next integration step:
1. Connect the existing server application to `provider_factory.build_registry()`.
2. Add `/api/providers`, `/api/jobs/{id}`, and provider-backed generation endpoints.
3. Patch the selected official ComfyUI API workflow through an explicit template adapter (no guessed node IDs).
4. Run a real short generation against a reachable GPU provider.
