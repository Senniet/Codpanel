from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from .schemas import Server, PowerRequest, FileEntry, BackupEntry, MetricsOut, ErrorResponse, StatusEnum, PowerActionEnum

router = APIRouter()

# Mocked server dataset
MOCK_SERVERS = [
    Server(id=1, name='COD-Server-1', ip='192.168.1.10', game='CoD', map='mp_shipment', players=12, cpu=25, ram=40, status=StatusEnum.running),
    Server(id=2, name='COD-Server-2', ip='192.168.1.11', game='CoD', map='mp_crossfire', players=0, cpu=2, ram=10, status=StatusEnum.stopped),
    Server(id=3, name='COD-Server-3', ip='192.168.1.12', game='CoD', map='mp_terminal', players=45, cpu=70, ram=80, status=StatusEnum.running),
]

@router.get('/servers', response_model=List[Server], responses={400: {'model': ErrorResponse}})
async def list_servers(q: str = '', status: str = ''):
    results = MOCK_SERVERS
    if q:
        ql = q.lower()
        results = [s for s in results if ql in s.name.lower() or ql in s.ip or ql in s.game.lower()]
    if status:
        # validate status value against StatusEnum
        try:
            st = StatusEnum(status)
        except ValueError:
            raise HTTPException(status_code=400, detail=ErrorResponse(code='invalid_parameter', message='Invalid status filter').dict())
        results = [s for s in results if s.status == st]
    return results

@router.get('/servers/{server_id}', response_model=Server, responses={404: {'model': ErrorResponse}})
async def get_server(server_id: int):
    for s in MOCK_SERVERS:
        if s.id == server_id:
            return s
    raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())

@router.post('/servers/{server_id}/power', response_model=dict, responses={400: {'model': ErrorResponse}, 404: {'model': ErrorResponse}})
async def perform_power(server_id: int, payload: PowerRequest):
    # Validate server exists
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    # payload.action is validated as PowerActionEnum by Pydantic
    if payload.action not in (PowerActionEnum.start, PowerActionEnum.stop, PowerActionEnum.restart, PowerActionEnum.kill):
        raise HTTPException(status_code=400, detail=ErrorResponse(code='invalid_action', message='Unknown action').dict())
    return {'result': 'ok'}

@router.get('/servers/{server_id}/overview', response_model=dict, responses={404: {'model': ErrorResponse}})
async def server_overview(server_id: int):
    for s in MOCK_SERVERS:
        if s.id == server_id:
            return {
                'game': s.game,
                'map': s.map,
                'players': s.players,
                'uptime': '3 days 4:12:00'
            }
    raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())

@router.get('/servers/{server_id}/console', response_model=List[str], responses={404: {'model': ErrorResponse}})
async def server_console(server_id: int):
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    return [
        '2026-01-01 12:00:00 Server starting...',
        '2026-01-01 12:00:05 Loading map mp_shipment',
        '2026-01-01 12:00:10 Server online'
    ]

@router.get('/servers/{server_id}/files', response_model=List[FileEntry], responses={404: {'model': ErrorResponse}})
async def server_files(server_id: int):
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    return [
        FileEntry(name='server.cfg', size=2345),
        FileEntry(name='maprotation.txt', size=123)
    ]

@router.get('/servers/{server_id}/config', response_model=dict, responses={404: {'model': ErrorResponse}})
async def server_config(server_id: int):
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    return {
        'max_players': 64,
        'rcon_password': 'changeme',
        'tickrate': 60
    }

@router.get('/servers/{server_id}/backups', response_model=List[BackupEntry], responses={404: {'model': ErrorResponse}})
async def server_backups(server_id: int):
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    now = datetime.utcnow()
    return [
        BackupEntry(name='backup-2026-06-30.tar.gz', created_at=now),
        BackupEntry(name='backup-2026-06-23.tar.gz', created_at=now)
    ]

@router.get('/servers/{server_id}/metrics', response_model=MetricsOut, responses={404: {'model': ErrorResponse}})
async def server_metrics(server_id: int):
    if not any(s.id == server_id for s in MOCK_SERVERS):
        raise HTTPException(status_code=404, detail=ErrorResponse(code='not_found', message='Server not found').dict())
    return MetricsOut(cpu_percent=72, memory_percent=65)
