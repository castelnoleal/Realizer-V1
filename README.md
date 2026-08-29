# Realizer V1

Realizer is a web-based text-to-video studio designed as a lightweight gateway for remote or local AI video generation.

## Architecture

`GitHub Pages / browser UI → generation backend → ComfyUI or hosted provider → MP4`

The browser UI is intentionally lightweight so it can run on low-power devices. AI inference is performed by a separate backend/GPU machine or hosted provider.

## Current capabilities

- Text-to-video project workflow
- Storyboard/scenes
- Generation queue
- Local ComfyUI integration
- Hosted-provider adapter
- Setup/readiness diagnostics
- Video retrieval and preview
- Responsive desktop/mobile UI

## Local backend

See `backend/README.md`. The backend requires Python and communicates with ComfyUI on the configured machine.

## Important

Do not put provider API keys or private credentials in the GitHub Pages frontend. Keep secrets in the backend environment.

## Roadmap

1. Image-to-video upload and generation
2. Start/end frame video
3. Automatic workflow mapping
4. Remote GPU deployment
5. Persistent project storage
6. End-to-end automated regression tests
