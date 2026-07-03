from fastapi import APIRouter, HTTPException, Response, Cookie
from pydantic import BaseModel
from typing import Optional

router = APIRouter()

class LoginRequest(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    email: Optional[str] = None

@router.post('/auth/login', response_model=UserOut)
async def login(payload: LoginRequest, response: Response):
    # Mocked authentication: only admin/admin is accepted
    if not (payload.username == 'admin' and payload.password == 'admin'):
        raise HTTPException(status_code=401, detail='Invalid credentials')

    # Set HttpOnly session cookie (mock)
    response.set_cookie(
        key='session',
        value='mock-session',
        httponly=True,
        samesite='lax',
        secure=False,
    )
    return UserOut(id=1, username=payload.username, email=f"{payload.username}@example.com")

@router.get('/auth/me', response_model=UserOut)
async def me(session: Optional[str] = Cookie(None)):
    if session != 'mock-session':
        raise HTTPException(status_code=401, detail='Not authenticated')
    return UserOut(id=1, username='admin', email='admin@example.com')

@router.post('/auth/logout')
async def logout(response: Response):
    # Clear the cookie
    response.delete_cookie('session')
    return {'success': True}
