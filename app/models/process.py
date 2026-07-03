from typing import Optional
from pydantic import BaseModel


class ProcessStats(BaseModel):
    """Runtime statistics for a system process."""

    pid: int
    cpu_percent: Optional[float] = None
    memory_mb: Optional[float] = None
    create_time: Optional[float] = None
    uptime_seconds: Optional[float] = None
