from fastapi import APIRouter
from game_app.services.table_service import get_table_bd, drop_db
from fastapi import HTTPException
router = APIRouter()

@router.post("/table/get_tables")
async def get_tables(payload: dict):
    game_type = payload.get("game_type")
    print("AAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAA")
    print("AAAAAAAAAAAAAA")
    try:
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        print("AAAAAAAAAAAAAA")
        tables = await get_table_bd(game_type)
        print(tables)
        return {"status": "success", "tables": tables}
    except ValueError as e:
        raise HTTPException(status_code=500, detail=e)