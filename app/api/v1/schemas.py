from enum import Enum
from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime

# Common enums
class StatusEnum(str, Enum):
    running = 'running'
    stopped = 'stopped'
    starting = 'starting'
    stopping = 'stopping'
    crashed = 'crashed'

class ActivityTypeEnum(str, Enum):
    info = 'info'
    warning = 'warning'
    error = 'error'

class LogLevelEnum(str, Enum):
    info = 'info'
    warning = 'warning'
    error = 'error'

class PowerActionEnum(str, Enum):
    start = 'start'
    stop = 'stop'
    restart = 'restart'
    kill = 'kill'

# Shared responses
class ErrorResponse(BaseModel):
    code: str
    message: str

class SuccessResponse(BaseModel):
    success: bool

class ActionResponse(BaseModel):
    result: str

# Auth models
class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

# Dashboard models
class DashboardOverview(BaseModel):
    totalServers: int
    onlineServers: int
    offlineServers: int
    connectedPlayers: int
    cpuUsagePercent: int
    memoryUsagePercent: int

class ActivityItem(BaseModel):
    id: int
    type: ActivityTypeEnum
    message: str
    created_at: datetime

class QuickAction(BaseModel):
    id: int
    name: str
    description: str

class LogEntry(BaseModel):
    id: int
    level: LogLevelEnum
    message: str
    timestamp: datetime

# Server models
class Server(BaseModel):
    id: int
    name: str
    ip: str
    game: str
    map: str
    players: int
    cpu: int
    ram: int
    status: StatusEnum

class PowerRequest(BaseModel):
    action: PowerActionEnum

class FileEntry(BaseModel):
    name: str
    size: int

class BackupEntry(BaseModel):
    name: str
    created_at: datetime

class MetricsOut(BaseModel):
    cpu_percent: int
    memory_percent: int
