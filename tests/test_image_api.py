from backend.image_store import ImageStore
from backend.providers import GenerationRequest

def test_allowed_image_types(tmp_path):
    s=ImageStore(tmp_path)
    p=s.save('image/png', b'fake-png')
    assert p.endswith('.png')

def test_reject_bad_type(tmp_path):
    s=ImageStore(tmp_path)
    try: s.save('text/plain', b'x')
    except ValueError as e: assert 'JPEG' in str(e)
    else: assert False

def test_reject_oversize(tmp_path):
    s=ImageStore(tmp_path)
    try: s.save('image/png', b'x'*(10*1024*1024+1))
    except ValueError as e: assert '10 MB' in str(e)
    else: assert False
