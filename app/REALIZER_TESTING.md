# Browser test checklist

Open `browser-test.html` from the GitHub Pages deployment.

1. Confirm `UI runtime` says PASS.
2. Select a JPG/PNG/WebP image and confirm preview + PASS.
3. Enter a prompt and select image mode; click Validate Request.
4. Set Backend endpoint to the running Realizer backend and click Test Backend.
5. The backend health response should report `ok: true` and `image_to_video_endpoint: true`.
6. Without ComfyUI, generation should fail cleanly with a setup/connection message; this is expected until a provider is configured.
7. With ComfyUI and an API-format workflow configured, run Setup Scan, Connection Test, then a short generation.
