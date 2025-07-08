from sqlalchemy import Column, Integer, String, Enum, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, relationship
import os
from pathlib import Path
import enum
from datetime import datetime

db_path = os.getenv("DB_PATH", str(Path(__file__).parent / "data" / "poker.db"))
os.makedirs(os.path.dirname(db_path), exist_ok=True)
engine = create_async_engine(f'sqlite+aiosqlite:///{db_path}')


new_session = async_sessionmaker(engine, expire_on_commit=False)

database = new_session()

class Base(DeclarativeBase):
    pass

class Table(Base):
    __tablename__ = "tables"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    game_type = Column(String)
    mode = Column(String)
    min_buy_in = Column(Integer)
    max_players = Column(Integer)
    current_players = Column(Integer, default=0)
    is_active = Column(Boolean, default=False)

    players = relationship("TablePlayer", back_populates="table")

    def update_activity_status(self):
        if self.mode == "tournament":
            self.is_active = self.current_players >= self.max_players
        else:
            self.is_active = self.current_players > 1

class TablePlayer(Base):
    __tablename__ = "table_players"

    id = Column(Integer, primary_key=True)
    table_id = Column(Integer, ForeignKey("tables.id"))
    user_id = Column(Integer)  # из auth/lobby
    joined_at = Column(DateTime, default=datetime.now())
    chips = Column(Integer)
    avatar = Column(String)

    table = relationship("Table", back_populates="players")
