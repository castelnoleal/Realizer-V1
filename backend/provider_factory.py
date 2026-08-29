from .providers import ProviderRegistry
from .comfyui_provider import ComfyUIProvider
from .remote_provider import RemoteProvider

def build_registry():
    r=ProviderRegistry()
    r.register(ComfyUIProvider())
    r.register(RemoteProvider())
    return r
