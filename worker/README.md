# Realizer Worker

The worker is the compute boundary for open models. It must run on a GPU-capable environment; the browser and lightweight backend do not need the model weights.

## Planned engines
- Wan 2.1 T2V 1.3B for Text → Video
- Wan 2.1 VACE 1.3B for Image/Reference/Video workflows

Model weights are downloaded at worker setup time from their official model repositories and are not committed to Git.

The worker API will expose health, model readiness, job submission, progress, cancellation, and output retrieval. The Realizer backend remains provider-neutral so the worker can later be moved to owned hardware without changing the browser application.
