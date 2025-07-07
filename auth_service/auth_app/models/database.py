from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
from pathlib import Path
import os

db_path = os.getenv("DB_PATH", str(Path(__file__).parent / "data" / "user.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}')
new_session = async_sessionmaker(engine, expire_on_commit=False)

database = new_session()

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(128), nullable=False)

async def init_db():
    """Создание всех таблиц при старте приложения"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
