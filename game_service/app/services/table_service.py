from sqlalchemy.ext.asyncio import AsyncSession

from models.database import Base, Table,TablePlayer, new_session, engine, Table
import pydantic
from sqlalchemy.future import select
from datetime import date

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def update_table_activity(table: Table, session: AsyncSession):
    table.update_activity_status()
    session.add(table)
    await session.commit()