from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


engine = create_async_engine('sqlite+aiosqlite:///user.db')

new_session = async_sessionmaker(engine, expire_on_commit=False)

database = new_session()

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    nickname = Column(String(50), nullable=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String(128), nullable=False)

