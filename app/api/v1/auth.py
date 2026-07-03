from fastapi import APIRouter, HTTPException, Response, Cookie
from typing import Optional
from .schemas import LoginRequest, UserOut, ErrorResponse

router = APIRouter()

# Constants
MOCK_SESSION_VALUE = 'mock-session'

@router.post('/auth/login', response_model=UserOut, responses={401: {'model': ErrorResponse}})
async def login(payload: LoginRequest, response: Response):
    # Mocked authentication: only admin/admin is accepted
    if not (payload.username == 'admin' and payload.password == 'admin'):
        raise HTTPException(status_code=401, detail=ErrorResponse(code='unauthorized', message='Invalid credentials').dict())

    # Set HttpOnly session cookie (mock)
    response.set_cookie(
        key='session',
        value=MOCK_SESSION_VALUE,
        httponly=True,
        samesite='lax',
        secure=False,
    )
    return UserOut(id=1, username=payload.username, email=f"{payload.username}@example.com")

@router.get('/auth/me', response_model=UserOut, responses={401: {'model': ErrorResponse}})
async def me(session: Optional[str] = Cookie(None)):
    if session != MOCK_SESSION_VALUE:
        raise HTTPException(status_code=401, detail=ErrorResponse(code='unauthenticated', message='Not authenticated').dict())
    return UserOut(id=1, username='admin', email='admin@example.com')

@router.post('/auth/logout', response_model=dict)
async def logout(response: Response):
    # Clear the cookie
    response.delete_cookie('session')
    return {'success': True}
