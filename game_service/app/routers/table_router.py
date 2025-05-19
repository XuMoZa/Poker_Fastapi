from fastapi import APIRouter

router = APIRouter()

router.post("/table/get_table", tags=["table"] )