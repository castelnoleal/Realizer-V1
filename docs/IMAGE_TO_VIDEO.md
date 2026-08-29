# Image → Video

Realizer V1 now has the complete browser/backend boundary for image-to-video input.

### Browser
`app/image-to-video.js` validates JPG/PNG/WebP, enforces the 10 MB limit, previews the image, and submits multipart form data.

### Backend
`backend/image_api.py` validates the upload again, stores it outside the Git repository, validates prompt/duration/FPS, and returns a normalized queued request.

### Provider
Actual inference is intentionally delegated to the configured provider adapter. This prevents the frontend from being coupled to ComfyUI and allows a remote GPU provider to be added later.
