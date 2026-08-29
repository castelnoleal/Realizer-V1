"""Provider-neutral generation contracts for Realizer V1."""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any

@dataclass
class GenerationRequest:
    mode: str = "text-to-video"
    prompt: str = ""
    negative_prompt: str = ""
    image_url: Optional[str] = None
    duration: float = 4.0
    fps: int = 16
    width: int = 832
    height: int = 480
    seed: Optional[int] = None

    def validate(self):
        if self.mode not in {"text-to-video", "image-to-video", "text-image-to-video"}:
            raise ValueError("Unsupported generation mode")
        if not self.prompt.strip():
            raise ValueError("Prompt is required")
        if self.mode != "text-to-video" and not self.image_url:
            raise ValueError("An image is required for image generation modes")
        if not 1 <= self.duration <= 30:
            raise ValueError("Duration must be between 1 and 30 seconds")
        if self.fps not in {8, 12, 16, 24, 25, 30}:
            raise ValueError("Unsupported FPS")
        return self

class Provider:
    name = "base"
    async def health(self) -> Dict[str, Any]:
        raise NotImplementedError
    async def generate(self, request: GenerationRequest) -> Dict[str, Any]:
        raise NotImplementedError
    async def status(self, job_id: str) -> Dict[str, Any]:
        raise NotImplementedError

class ProviderRegistry:
    def __init__(self): self._providers = {}
    def register(self, provider: Provider): self._providers[provider.name] = provider
    def get(self, name):
        if name not in self._providers: raise KeyError(f"Provider not configured: {name}")
        return self._providers[name]
    def names(self): return sorted(self._providers)
