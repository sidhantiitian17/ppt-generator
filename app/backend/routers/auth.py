from __future__ import annotations

from uuid import uuid4

from fastapi import APIRouter, HTTPException, status

from ..models.deck import AuthRequest, AuthResponse

router = APIRouter()

_users: dict[str, str] = {}
_tokens: dict[str, str] = {}


@router.post("/signup", response_model=AuthResponse)
async def signup(payload: AuthRequest) -> AuthResponse:
    if payload.email in _users:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    _users[payload.email] = payload.password
    token = uuid4().hex
    _tokens[token] = payload.email
    return AuthResponse(access_token=token)


@router.post("/login", response_model=AuthResponse)
async def login(payload: AuthRequest) -> AuthResponse:
    stored = _users.get(payload.email)
    if stored != payload.password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = uuid4().hex
    _tokens[token] = payload.email
    return AuthResponse(access_token=token)
