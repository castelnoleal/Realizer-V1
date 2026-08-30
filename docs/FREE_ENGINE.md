# Realizer Free Engine

Realizer V1 uses open model weights as its default model layer. This does not mean GPU compute is free; the application separates model licensing from compute infrastructure.

The initial free/open model layer is Wan 2.1. T2V-1.3B is Apache-2.0 and supports text-to-video at 480p. VACE-1.3B is Apache-2.0 and supports image/reference/video-conditioned workflows. The official model cards document Diffusers integration and GPU inference requirements.

Realizer's subscription product can charge for the hosted service, storage, queue priority, and compute while preserving the open model layer. Commercial deployment must still comply with each model's license and any infrastructure provider terms.
