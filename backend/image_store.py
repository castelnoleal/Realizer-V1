"""Upload validation/storage boundary for image-to-video jobs."""
from pathlib import Path
import uuid

ALLOWED={"image/jpeg":".jpg","image/png":".png","image/webp":".webp"}
MAX_BYTES=10*1024*1024

class ImageStore:
    def __init__(self, root="storage/uploads"):
        self.root=Path(root); self.root.mkdir(parents=True,exist_ok=True)
    def save(self, content_type: str, data: bytes):
        if content_type not in ALLOWED: raise ValueError("Only JPEG, PNG and WebP images are supported")
        if len(data)>MAX_BYTES: raise ValueError("Image exceeds 10 MB limit")
        name=uuid.uuid4().hex+ALLOWED[content_type]
        path=self.root/name; path.write_bytes(data)
        return str(path)
