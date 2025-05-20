from fastapi import APIRouter, Request, Form, HTTPException, status
import pydantic
from starlette.responses import HTMLResponse
from services .auth_service import drop_db, create_user, authenticate_user, user_id_by_email
from core.settings import security
from datetime import date, datetime

router = APIRouter()


@router.post("/auth/pre_registrate")
async def registration_success(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    try:

        new_user = await create_user(email=email, password=password)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("auth/authorization")
async def authorization_success(payload: dict):
    email = payload.get("email")
    password = payload.get("password")
    try:
        user = await authenticate_user(email = email, password = password)
        if user:
            return {"status": "success", "user_id": user.id}
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
