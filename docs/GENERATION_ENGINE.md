# Realizer V1 Generation Engine

## Modes
- Text → Video
- Image → Video
- Text + Image → Video

## Provider boundary
The browser sends a normalized generation request to the backend. Providers implement `health`, `generate`, and `status`. This keeps the UI independent from ComfyUI or any hosted GPU vendor.

## Image pipeline
Images are validated for MIME type and size at the backend boundary. The browser previews locally; the backend stores the generation input before handing it to a provider.

## Local inference
ComfyUI is an optional provider. Model weights and API workflow JSON are intentionally not committed to Git.

## Remote inference
A hosted provider can be added without changing the UI contract. Secrets belong in the server environment, never in browser JavaScript.

## Job lifecycle
`queued → running → completed | failed | cancelled`

Outputs are represented by a provider-neutral `output_url`.
