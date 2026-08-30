# Free-model architecture

Realizer V1 now treats open model weights and compute infrastructure as separate concerns.

The primary model is Wan 2.1 T2V 1.3B (Apache-2.0). The Wan 2.1 VACE 1.3B model is registered for future image/reference/video workflows.

The browser never downloads or executes model weights. It calls the Realizer backend. The backend can dispatch to a self-hosted GPU worker using Diffusers/ComfyUI. This preserves a browser-first product while avoiding a mandatory paid inference API.

**Important:** free/open weights do not make GPU compute free. The application must not claim "free generation" until a no-cost compute route is actually configured. The product can nevertheless use these models without per-generation model licensing/API fees.
