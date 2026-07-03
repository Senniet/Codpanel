from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Any
from datetime import datetime

router = APIRouter()

class Server(BaseModel):
    id: int
    name: str
    ip: str
    game: str
    map: str
    players: int
    cpu: int
    ram: int
    status: str

class ActionRequest(BaseModel):
    action: str

class FileEntry(BaseModel):
    name: str
    size: int

class BackupEntry(BaseModel):
    name: str
    created_at: datetime

class MetricsOut(BaseModel):
    cpu_percent: int
    memory_percent: int

# Mocked server dataset
MOCK_SERVERS = [
    Server(id=1, name='COD-Server-1', ip='192.168.1.10', game='CoD', map='mp_shipment', players=12, cpu=25, ram=40, status='running'),
    Server(id=2, name='COD-Server-2', ip='192.168.1.11', game='CoD', map='mp_crossfire', players=0, cpu=2, ram=10, status='stopped'),
    Server(id=3, name='COD-Server-3', ip='192.168.1.12', game='CoD', map='mp_terminal', players=45, cpu=70, ram=80, status='running'),
]

@router.get('/servers', response_model=List[Server])
async def list_servers(q: str = '', status: str = ''):
    results = MOCK_SERVERS
    if q:
        ql = q.lower()
        results = [s for s in results if ql in s.name.lower() or ql in s.ip or ql in s.game.lower()]
    if status:
        results = [s for s in results if s.status == status]
    return results

@router.get('/servers/{server_id}', response_model=Server)
async def get_server(server_id: int):
    for s in MOCK_SERVERS:
        if s.id == server_id:
            return s
    raise HTTPException(status_code=404, detail='Server not found')

@router.post('/servers/{server_id}/actions')
async def perform_action(server_id: int, payload: ActionRequest):
    # Mock: accept action but do not change state
    # Validate server exists
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail='Server not found')
    if payload.action not in ('start', 'stop', 'restart', 'kill'):
        raise HTTPException(status_code=400, detail='Unknown action')
    return {'result': 'ok'}

@router.get('/servers/{server_id}/overview')
async def server_overview(server_id: int):
    # Return mocked overview
    return {
        'game': 'CoD',
        'map': 'mp_shipment',
        'players': 12,
        'uptime': '3 days 4:12:00'
    }

@router.get('/servers/{server_id}/console')
async def server_console(server_id: int):
    # Mocked console lines
    return [
        '2026-01-01 12:00:00 Server starting...',
        '2026-01-01 12:00:05 Loading map mp_shipment',
        '2026-01-01 12:00:10 Server online'
    ]

@router.get('/servers/{server_id}/files', response_model=List[FileEntry])
async def server_files(server_id: int):
    return [
        FileEntry(name='server.cfg', size=2345),
        FileEntry(name='maprotation.txt', size=123)
    ]

@router.get('/servers/{server_id}/config')
async def server_config(server_id: int):
    return {
        'max_players': 64,
        'rcon_password': 'changeme',
        'tickrate': 60
    }

@router.get('/servers/{server_id}/backups', response_model=List[BackupEntry])
async def server_backups(server_id: int):
    now = datetime.utcnow()
    return [
        BackupEntry(name='backup-2026-06-30.tar.gz', created_at=now),
        BackupEntry(name='backup-2026-06-23.tar.gz', created_at=now)
    ]

@router.get('/servers/{server_id}/metrics', response_model=MetricsOut)
async def server_metrics(server_id: int):
    return MetricsOut(cpu_percent=72, memory_percent=65)
