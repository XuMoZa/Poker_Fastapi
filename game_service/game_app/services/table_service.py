from sqlalchemy.ext.asyncio import AsyncSession

from game_app.models.database import Base, Table,TablePlayer, new_session, engine, Table
import pydantic
from sqlalchemy.future import select
from datetime import date
from sqlalchemy import Boolean

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_table_bd(game_type: str):
    async with new_session() as session:
        stmt = select(Table).where(Table.game_type == game_type)
        result = await session.execute(stmt)
        tables = result.scalars().all()
    return tables