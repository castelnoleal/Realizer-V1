import asyncio
from backend.provider_factory import build_registry
from backend.providers import GenerationRequest

def test_registry_has_providers():
    r=build_registry()
    assert 'comfyui' in r.names()
    assert 'remote' in r.names()

def test_remote_unconfigured_health():
    p=build_registry().get('remote')
    result=asyncio.run(p.health())
    assert result['configured'] is False

def test_comfyui_workflow_missing_fails_cleanly(tmp_path):
    p=build_registry().get('comfyui')
    p.workflow_path=str(tmp_path/'missing.json')
    try:
        asyncio.run(p.generate(GenerationRequest(prompt='test')))
    except RuntimeError as e:
        assert 'Workflow not found' in str(e)
    else:
        assert False
