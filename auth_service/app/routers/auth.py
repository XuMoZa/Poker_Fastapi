from fastapi import APIRouter, Request, Form, HTTPException, status
import pydantic
from starlette.responses import HTMLResponse
from services .user_service import drop_db, create_user, no_info_user, add_user_info, authenticate_user
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

@router.post("/auth/registrate")
async def registration_with_info(payload: dict):

    email = payload.get("email")
    name = payload.get("name")
    last_name = payload.get("last_name")
    birthday = payload.get("birthday")
    nickname = payload.get("nickname")
    date_obj = datetime.strptime(birthday, "%Y-%m-%d")
    try:
        edit_user = await add_user_info(email=email, name=name, last_name=last_name, birthday=date_obj, nickname=nickname)
        return {"status": "success", "id": edit_user.id}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
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
