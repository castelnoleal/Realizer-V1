# Realizer providers

Realizer supports two provider boundaries now:

- **ComfyUI**: points at a running ComfyUI HTTP server and consumes an API-format workflow exported from that installation. No workflow node IDs are guessed.
- **Remote**: generic HTTP provider for a GPU service. The URL/token are server-side environment variables.

This separation means the Fujitsu tablet only needs the browser UI; inference can happen on another GPU machine or hosted service.

## ComfyUI configuration

Set:

`COMFYUI_URL=http://127.0.0.1:8188`

`COMFYUI_WORKFLOW_JSON=/absolute/path/to/exported-api-workflow.json`

The repository deliberately does not include model weights, provider secrets, or a version-specific workflow graph.
