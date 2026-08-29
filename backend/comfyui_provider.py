"""Provider adapter for a running ComfyUI HTTP server.

It intentionally accepts an API-format workflow exported by the user's ComfyUI
installation rather than embedding a version-specific graph in the repository.
"""
import json, os, uuid
from pathlib import Path
import httpx
from .providers import Provider, GenerationRequest

class ComfyUIProvider(Provider):
    name = 'comfyui'
    def __init__(self, base_url=None, workflow_path=None):
        self.base_url=(base_url or os.getenv('COMFYUI_URL','http://127.0.0.1:8188')).rstrip('/')
        self.workflow_path=workflow_path or os.getenv('COMFYUI_WORKFLOW_JSON','')
    async def health(self):
        async with httpx.AsyncClient(timeout=8) as c:
            r=await c.get(self.base_url+'/system_stats'); r.raise_for_status()
            return {'ok':True,'provider':self.name,'base_url':self.base_url,'system':r.json()}
    def _workflow(self):
        if not self.workflow_path: raise RuntimeError('COMFYUI_WORKFLOW_JSON is not configured')
        p=Path(self.workflow_path)
        if not p.exists(): raise RuntimeError(f'Workflow not found: {p}')
        data=json.loads(p.read_text(encoding='utf-8'))
        if not isinstance(data,dict): raise RuntimeError('Workflow must be an API-format JSON object')
        return data
    async def generate(self, request: GenerationRequest):
        wf=self._workflow()
        # The adapter does not guess node IDs. A future template adapter can patch
        # known official workflow node inputs safely. For now, preserve the graph.
        client_id=str(uuid.uuid4())
        async with httpx.AsyncClient(timeout=20) as c:
            r=await c.post(self.base_url+'/prompt',json={'prompt':wf,'client_id':client_id})
            r.raise_for_status(); data=r.json()
        if 'prompt_id' not in data: raise RuntimeError(f'ComfyUI did not return prompt_id: {data}')
        return {'provider':self.name,'job_id':data['prompt_id'],'client_id':client_id,'status':'queued'}
    async def status(self, job_id):
        async with httpx.AsyncClient(timeout=10) as c:
            r=await c.get(self.base_url+'/history/'+job_id); r.raise_for_status(); data=r.json()
        item=data.get(job_id)
        if not item: return {'status':'queued','progress':0}
        status=item.get('status',{})
        if status.get('status_str') == 'error': return {'status':'failed','error':status.get('messages')}
        outputs=item.get('outputs') or {}
        files=[]
        for node in outputs.values():
            for key in ('gifs','videos','images'):
                for f in node.get(key,[]) or []:
                    files.append(f)
        if files: return {'status':'completed','progress':100,'files':files}
        return {'status':'running','progress':50}
