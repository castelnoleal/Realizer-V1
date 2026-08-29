from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from .image_store import ImageStore

router = APIRouter(prefix='/api/generate')
store = ImageStore()

@router.post('/image-to-video')
async def image_to_video(
    image: UploadFile = File(...),
    prompt: str = Form(...),
    negative_prompt: str = Form(''),
    duration: float = Form(4.0),
    fps: int = Form(16),
):
    if image.content_type not in {'image/jpeg','image/png','image/webp'}:
        raise HTTPException(415, 'Only JPEG, PNG and WebP images are supported.')
    data = await image.read()
    try:
        path = store.save(image.content_type, data)
    except ValueError as e:
        raise HTTPException(400, str(e)) from e
    if not prompt.strip():
        raise HTTPException(400, 'Motion prompt is required.')
    if not 1 <= duration <= 30:
        raise HTTPException(400, 'Duration must be between 1 and 30 seconds.')
    if fps not in {8,12,16,24,25,30}:
        raise HTTPException(400, 'Unsupported FPS.')
    # Provider dispatch is intentionally separate: this endpoint owns validation/storage,
    # while configured providers own actual inference.
    return {'accepted': True, 'mode':'image-to-video', 'input_path':path,
            'prompt':prompt.strip(), 'negative_prompt':negative_prompt,
            'duration':duration, 'fps':fps, 'status':'queued'}
