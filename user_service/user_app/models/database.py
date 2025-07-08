from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session
import os
from pathlib import Path


db_path = os.getenv("DB_PATH", str(Path(__file__).parent / "data" / "profile.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}')

new_session = async_sessionmaker(engine, expire_on_commit=False)

database = new_session()

class Base(DeclarativeBase):
    pass

class Profile(Base):
    __tablename__ = "profile"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, unique=True)
    name = Column(String)
    last_name = Column(String)
    age = Column(Integer)
    avatar_url = Column(String)

