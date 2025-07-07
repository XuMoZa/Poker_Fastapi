from auth_app.models.database import Base, User, new_session, engine
import pydantic
from sqlalchemy.future import select
from sqlalchemy import or_
from datetime import date
import bcrypt

async def get_all_users():
    async with new_session() as session:
        stmt = select(User)
        result = await session.execute(stmt)
        users = result.scalars().all()
        return users

async def create_user(email:pydantic.EmailStr, nickname:str, password:str):
    async with new_session() as session:
        stmt = select(User).where(
            or_(
                User.email == email,
                User.nickname == nickname
            )
        )
        result = await session.execute(stmt)
        print(result)
        password = str(password)
        existing_user = result.scalars().first()
        email = str(email)
        print(existing_user)
        if existing_user:
            raise ValueError("Пользователь с таким именем или email уже существует.")
        hashed_password = hash_password(password)
        new_user = User(email=email, password=hashed_password, nickname=nickname)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def edit_user_info(name:str, last_name:str, birthday:date, nickname:str, email:str ):
    async with new_session() as session:
        new_user = User(email=email)
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user

async def authenticate_user(email:str, password:str):
    user : User = await get_user_by_email(email)
    if not user:
        return False
    if verify_password(password=password, hashed_password=user.password):
        return user.id
    else:
        return False

async def user_id_by_email(email:str):
    user : User = await get_user_by_email(email)
    if not user: return False
    else: return user.id

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

def hash_password(password: str) -> str:
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

async def get_user_by_email(email:str):
    async with new_session() as session:
        stmt = select(User).where((User.email == email))
        result = await session.execute(stmt)
        user: User = result.scalars().first()
    return user