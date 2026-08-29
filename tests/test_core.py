import asyncio
from backend.providers import GenerationRequest
from backend.job_store import JobStore, Job

def test_text_request():
    r=GenerationRequest(prompt="a cinematic ocean at sunset").validate()
    assert r.mode == "text-to-video"

def test_image_request_requires_image():
    try: GenerationRequest(mode="image-to-video", prompt="animate it").validate()
    except ValueError as e: assert "image" in str(e).lower()
    else: assert False

def test_image_request_accepts_image():
    GenerationRequest(mode="image-to-video", prompt="animate it", image_url="/uploads/a.png").validate()

def test_job_store():
    s=JobStore(); s.put(Job("abc",provider="comfyui")); s.update("abc",progress=50,status="running")
    assert s.snapshot("abc")["progress"] == 50
