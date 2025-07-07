from fastapi import APIRouter
from services.table_service import get_table_bd, drop_db
from fastapi import HTTPException
router = APIRouter()

@router.post("/table/get_table")
async def get_tables(payload: dict):
    game_type = payload.get("game_type")
    try:

        tables = await get_table_bd(game_type)
        return {"status": "success", "tables": tables}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=e)