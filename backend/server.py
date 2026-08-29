import os
import json
import time
import uuid
from pathlib import Path

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

app = FastAPI(title="Realizer V1 Backend", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_credentials=False, allow_methods=["*"], allow_headers=["*"])
JOBS={}

def comfy_url(): return os.getenv("COMFYUI_URL","http://127.0.0.1:8188").rstrip('/')
def comfy_reachable():
    try: return requests.get(comfy_url()+"/system_stats",timeout=3).ok
    except Exception: return False

def ratio_size(r,q):
    return {('16:9','480p'):(832,480),('16:9','720p'):(1280,720),('16:9','1080p'):(1920,1080),('9:16','480p'):(480,832),('9:16','720p'):(720,1280),('9:16','1080p'):(1080,1920),('1:1','480p'):(624,624),('1:1','720p'):(960,960),('1:1','1080p'):(1440,1440),('4:5','480p'):(576,720),('4:5','1080p'):(864,1080),('4:5','1080p'):(1296,1620)}.get((r,q),(1280,720))

class GenerateRequest(BaseModel):
    prompt:str=Field(min_length=1,max_length=12000)
    negative_prompt:str=''
    duration:int=Field(default=5,ge=1,le=60)
    fps:int=Field(default=24,ge=8,le=60)
    aspect_ratio:str='16:9'
    quality:str='720p'
    camera:str='Auto'
    model:str='Local ComfyUI'
    scenes:list=[]

def load_workflow():
    p=os.getenv('COMFYUI_WORKFLOW_JSON','').strip()
    if not p: raise RuntimeError('COMFYUI_WORKFLOW_JSON is not configured. Export an API-format Wan 2.2 workflow from ComfyUI and configure it on the backend.')
    path=Path(p)
    if not path.exists(): raise RuntimeError(f'Workflow file not found: {path}')
    return json.loads(path.read_text(encoding='utf-8'))

def patch_workflow(wf,req):
    wf=json.loads(json.dumps(wf)); prompt=req.prompt + (f'\nCamera movement: {req.camera}.' if req.camera!='Auto' else '')
    negative=req.negative_prompt or 'blurry, distorted, flicker, duplicate subjects, bad anatomy'
    width,height=ratio_size(req.aspect_ratio,req.quality); frames=max(9,min(241,round(req.duration*req.fps/4)*4+1))
    for node in wf.values():
        if not isinstance(node,dict): continue
        inp=node.get('inputs',{}); cls=str(node.get('class_type','')).lower()
        if 'cliptextencode' in cls and isinstance(inp.get('text'),str):
            inp['text']=negative if 'negative' in cls else prompt
        for k in list(inp):
            lk=str(k).lower()
            if lk in ('width','video_width') and isinstance(inp[k],(int,float)): inp[k]=width
            elif lk in ('height','video_height') and isinstance(inp[k],(int,float)): inp[k]=height
            elif lk in ('length','num_frames','frames','video_frames') and isinstance(inp[k],(int,float)): inp[k]=frames
            elif lk in ('frame_rate','fps') and isinstance(inp[k],(int,float)): inp[k]=req.fps
    return wf

def queue_comfy(wf):
    pid=str(uuid.uuid4()); r=requests.post(comfy_url()+'/prompt',json={'prompt':wf,'client_id':pid},timeout=30)
    if not r.ok: raise RuntimeError(f'ComfyUI /prompt HTTP {r.status_code}: {r.text[:500]}')
    d=r.json(); return d.get('prompt_id') or (_ for _ in ()).throw(RuntimeError('ComfyUI returned no prompt_id'))

def history(pid):
    try:
        r=requests.get(comfy_url()+'/history/'+pid,timeout=15)
        return r.json().get(pid) if r.ok else None
    except Exception: return None

def video_url_from_history(h):
    if not h: return None
    for node in h.get('outputs',{}).values():
        for key in ('gifs','videos'):
            for item in node.get(key,[]) if isinstance(node.get(key,[]),list) else []:
                if item.get('filename'):
                    from urllib.parse import quote
                    return '/api/comfy-file?filename='+quote(item['filename'])+'&subfolder='+quote(item.get('subfolder',''))+'&type='+quote(item.get('type','output'))
    return None

@app.get('/api/health')
def health(): return {'ok':True,'service':'realizer-backend','version':'1.0.0','comfyui_reachable':comfy_reachable()}

@app.get('/api/setup/scan')
def scan():
    out={'backend':True,'comfyui':{'reachable':False,'url':comfy_url()},'system':None,'models':{'detected':{'wan5b':False,'wan14b':False,'umt5':False,'wan_vae':False}},'recommendation':'Start ComfyUI to enable local generation.'}
    try:
        r=requests.get(comfy_url()+'/system_stats',timeout=4)
        if r.ok: out['comfyui']['reachable']=True; out['system']=r.json()
    except Exception: pass
    if not out['comfyui']['reachable']: return out
    try:
        r=requests.get(comfy_url()+'/models',timeout=8); models=r.json() if r.ok else {}
        names=[]
        for group in models.values() if isinstance(models,dict) else []:
            if isinstance(group,list): names += [x.get('name',x) if isinstance(x,dict) else x for x in group]
        s=' '.join(map(str,names)).lower(); d=out['models']['detected']
        d['wan5b']='wan2.2_ti2v_5b' in s; d['wan14b']='wan2.2' in s and '14b' in s; d['umt5']='umt5' in s; d['wan_vae']='wan' in s and 'vae' in s
        out['recommendation']='READY: compatible Wan model components detected.' if (d['wan5b'] or d['wan14b']) else 'ComfyUI is connected, but compatible Wan model files were not detected.'
    except Exception: out['recommendation']='ComfyUI connected; model scan failed.'
    return out

@app.get('/api/setup/requirements')
def requirements():
    return {'official_template':'Wan2.2 5B video generation','template_location':'ComfyUI → Workflow → Browse Templates → Video','models':['wan2.2_ti2v_5B_fp16.safetensors','wan2.2_vae.safetensors','umt5_xxl_fp8_e4m3fn_scaled.safetensors'],'notes':'Use the current official ComfyUI Wan workflow and export it as API-format JSON. Keep provider secrets server-side.'}

@app.post('/api/setup/test')
def setup_test():
    if not comfy_reachable(): raise HTTPException(503,'ComfyUI is not reachable.')
    p=os.getenv('COMFYUI_WORKFLOW_JSON','').strip()
    if not p: return {'ok':True,'level':'connection','message':'ComfyUI is reachable. Configure an API-format workflow to run a generation test.'}
    try:
        pid=queue_comfy(patch_workflow(load_workflow(),GenerateRequest(prompt='Realizer connection test',duration=1,fps=8,quality='480p'))); JOBS[pid]={'status':'queued','progress':0,'test':True}; return {'ok':True,'level':'generation','job_id':pid,'message':'Test job submitted.'}
    except Exception as e: raise HTTPException(502,str(e))

@app.post('/api/generate')
def generate(req:GenerateRequest):
    if req.model=='Hugging Face Provider': raise HTTPException(501,'Hosted provider generation requires a configured provider implementation.')
    if not comfy_reachable(): raise HTTPException(503,'Local ComfyUI is not reachable.')
    try:
        pid=queue_comfy(patch_workflow(load_workflow(),req)); JOBS[pid]={'status':'queued','progress':0,'created':time.time()}; return {'job_id':pid,'status':'queued'}
    except Exception as e: raise HTTPException(502,str(e))

@app.get('/api/jobs/{pid}')
def job_status(pid:str):
    h=history(pid); url=video_url_from_history(h)
    if url: JOBS[pid]={'status':'completed','progress':100}; return {'status':'completed','progress':100,'video_url':url}
    if h and h.get('status',{}).get('status_str')=='error': return {'status':'failed','progress':100,'error':str(h.get('status',{}).get('messages','ComfyUI generation failed.'))}
    j=JOBS.get(pid,{'status':'processing','progress':10}); j['status']='processing' if j['status']=='queued' else j['status']; JOBS[pid]=j; return j

@app.get('/api/comfy-file')
def comfy_file(filename:str,subfolder:str='',type:str='output'):
    try:
        r=requests.get(comfy_url()+'/view',params={'filename':filename,'subfolder':subfolder,'type':type},timeout=60)
        if not r.ok: raise HTTPException(r.status_code,'ComfyUI file request failed.')
        return Response(content=r.content,media_type=r.headers.get('content-type','video/mp4'))
    except HTTPException: raise
    except Exception as e: raise HTTPException(502,str(e))

if __name__=='__main__':
    import uvicorn; uvicorn.run(app,host='0.0.0.0',port=8000)
