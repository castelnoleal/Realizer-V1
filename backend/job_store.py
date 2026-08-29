"""Small in-process job store; replaceable by Redis/DB later."""
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional
import threading

@dataclass
class Job:
    id: str
    status: str = "queued"
    progress: float = 0.0
    provider: str = ""
    output_url: Optional[str] = None
    error: Optional[str] = None
    created_at: str = ""
    updated_at: str = ""

class JobStore:
    def __init__(self): self.jobs={}; self.lock=threading.Lock()
    def put(self, job: Job):
        now=datetime.now(timezone.utc).isoformat()
        job.created_at=job.created_at or now; job.updated_at=now
        with self.lock: self.jobs[job.id]=job
        return job
    def update(self, job_id, **changes):
        with self.lock:
            job=self.jobs[job_id]
            for k,v in changes.items(): setattr(job,k,v)
            job.updated_at=datetime.now(timezone.utc).isoformat()
            return job
    def get(self, job_id):
        with self.lock: return self.jobs.get(job_id)
    def snapshot(self, job_id):
        j=self.get(job_id)
        return asdict(j) if j else None
