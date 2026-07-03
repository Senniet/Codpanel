from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
from datetime import datetime

router = APIRouter()

class DashboardOverview(BaseModel):
    totalServers: int
    onlineServers: int
    offlineServers: int
    connectedPlayers: int
    cpuUsagePercent: int
    memoryUsagePercent: int

class ActivityItem(BaseModel):
    id: int
    type: str
    message: str
    created_at: datetime

class QuickAction(BaseModel):
    id: int
    name: str
    description: str

class LogEntry(BaseModel):
    id: int
    level: str
    message: str
    timestamp: datetime

@router.get('/dashboard/overview', response_model=DashboardOverview)
async def overview():
    # Return mocked overview data
    return DashboardOverview(
        totalServers=3,
        onlineServers=2,
        offlineServers=1,
        connectedPlayers=57,
        cpuUsagePercent=42,
        memoryUsagePercent=61
    )

@router.get('/dashboard/activity', response_model=List[ActivityItem])
async def activity():
    now = datetime.utcnow()
    items = [
        ActivityItem(id=1, type='info', message='Server COD-1 restarted', created_at=now),
        ActivityItem(id=2, type='warning', message='High memory usage on COD-2', created_at=now),
    ]
    return items

@router.get('/dashboard/quick-actions', response_model=List[QuickAction])
async def quick_actions():
    items = [
        QuickAction(id=1, name='Restart All Servers', description='Restart all game servers in sequence'),
        QuickAction(id=2, name='Clear Cache', description='Clear application caches'),
    ]
    return items

@router.get('/dashboard/logs', response_model=List[LogEntry])
async def logs():
    now = datetime.utcnow()
    entries = [
        LogEntry(id=1, level='info', message='Server COD-1 booted', timestamp=now),
        LogEntry(id=2, level='error', message='Crash detected on COD-3', timestamp=now),
    ]
    return entries
