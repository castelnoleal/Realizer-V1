"""Generic remote-provider adapter contract.

Provider-specific API details are configured server-side; no credentials belong in the UI.
"""
import os, httpx
from .providers import Provider, GenerationRequest

class RemoteProvider(Provider):
    name='remote'
    def __init__(self, base_url=None, token=None):
        self.base_url=(base_url or os.getenv('REALIZER_REMOTE_URL','')).rstrip('/')
        self.token=token or os.getenv('REALIZER_REMOTE_TOKEN','')
    async def health(self):
        if not self.base_url: return {'ok':False,'provider':self.name,'configured':False}
        headers={'Authorization':f'Bearer {self.token}'} if self.token else {}
        async with httpx.AsyncClient(timeout=8) as c:
            r=await c.get(self.base_url+'/health',headers=headers); r.raise_for_status()
            return {'ok':True,'provider':self.name,'configured':True,'details':r.json()}
    async def generate(self, request: GenerationRequest):
        if not self.base_url: raise RuntimeError('REALIZER_REMOTE_URL is not configured')
        headers={'Authorization':f'Bearer {self.token}'} if self.token else {}
        async with httpx.AsyncClient(timeout=30) as c:
            r=await c.post(self.base_url+'/generate',json=request.__dict__,headers=headers); r.raise_for_status()
            data=r.json()
        if not data.get('job_id'): raise RuntimeError('Remote provider did not return job_id')
        return {'provider':self.name,**data}
    async def status(self, job_id):
        headers={'Authorization':f'Bearer {self.token}'} if self.token else {}
        async with httpx.AsyncClient(timeout=15) as c:
            r=await c.get(self.base_url+'/jobs/'+job_id,headers=headers); r.raise_for_status(); return r.json()
