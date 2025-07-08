from fastapi import APIRouter
from datetime import datetime
from fastapi import HTTPException

from user_app.services.user_service import drop_db, add_user, get_profile

router = APIRouter()

@router.post("/user/add_info")
async def add_user_info(payload : dict):
    name = payload.get("name")
    last_name = payload.get("last_name")
    birthday = payload.get("birthday")
    user_id = payload.get("user_id")
    date_obj = datetime.strptime(birthday, "%Y-%m-%d")
    try:
        await add_user(user_id=user_id, name=name, last_name=last_name, birthday=date_obj)
        return {"status": "success"}
    except ValueError as e:
        raise HTTPException(status_code=401, detail="Invalid credentials")

@router.post("/user/info")
async def user_info(payload: dict):
    user_id = payload.get("user_id")
    user = await get_profile(user_id=user_id)
    return {"user_id": user}
