"""Free/open-model provider boundary.

This adapter deliberately separates model ownership from compute hosting.
It can later call local Diffusers, ComfyUI, or a self-hosted GPU worker
without changing the browser API.
"""
from .model_registry import get_model

class FreeModelProvider:
    name = 'realizer-free'

    def health(self):
        return {'provider': self.name, 'model': get_model('wan2.1-t2v-1.3b'), 'compute_configured': False}

    def generate(self, request):
        # No fake generation: actual inference is enabled only when a worker is configured.
        raise RuntimeError('Realizer Free model is registered but no GPU inference worker is configured yet.')
