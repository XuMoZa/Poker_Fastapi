from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, sessionmaker, Session


engine = create_async_engine('sqlite+aiosqlite:///profile.db')

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

