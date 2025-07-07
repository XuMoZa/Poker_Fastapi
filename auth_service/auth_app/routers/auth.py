from fastapi import APIRouter, Request, Form, HTTPException, status
import pydantic
from starlette.responses import HTMLResponse
from auth_app.services.auth_service import drop_db, create_user, authenticate_user, user_id_by_email, get_all_users
from auth_app.models.database import drop_db
from auth_app.core.settings import security
from datetime import date, datetime

router = APIRouter()

@router.get("/health")
async def health_check():
    return {"status": "ok"}

@router.post("/auth/pre_registrate")
async def registration_success(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    nickname = payload.get("nickname")
    try:

        new_user = await create_user(email=email, password=password, nickname=nickname)
        return {"status": "success"}
    except ValueError as e:
        return {"status": "failed", "message": "Пользователь с таким именем или email уже существует."}

@router.get("/auth/users")
async def get_users():
    users = await get_all_users()
    return {"users": users}

@router.post("/auth/authorization")
async def authorization_success(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    try:
        user = await authenticate_user(email = email, password = password)
        if user:
            return {"status": "success", "user_id": user}
        else:
            return {"status": "error", "message": "Invalid credentials"}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/auth/get_id")
async def get_id_success(payload: dict):
    email = payload.get("email")
    user_id = await user_id_by_email(email)
    if user_id:
        return {"status": "success", "id": user_id}
    else:
        return {"status": "error", "message": "No user found"}
