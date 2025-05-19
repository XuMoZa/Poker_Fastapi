from models.database import Base, User, new_session, engine
import pydantic
from sqlalchemy.future import select
from datetime import date
import bcrypt

async def create_user(email:pydantic.EmailStr, password:str):
    async with new_session() as session:
        stmt = select(User).where((User.email == email))
        result = await session.execute(stmt)
        existing_user = result.scalar_one_or_none()
        if existing_user:
            raise ValueError("Пользователь с таким именем или email уже существует.")
        hashed_password = hash_password(password)
        new_user = User(email=email, password=hashed_password)
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

async def no_info_user(email:str):
    async with new_session() as session:
        stmt  = select(User).where((User.email == email))
        result = await session.execute(stmt)
        user : User = result.scalars().first()
        if any(not field for field in [user.name, user.nickname, user.last_name, user.age]):
            return True
        else:
            return False

async def add_user_info (name:str, last_name:str, birthday:date, email:str, nickname:str):
    async with new_session() as session:

        stmt = select(User).where((User.email == email))
        result = await session.execute(stmt)
        user: User = result.scalars().first()

        user.name = name
        user.nickname = nickname
        user.last_name = last_name

        if (date.today().month, date.today().day) < (birthday.month, birthday.day):
            user.age = date.today().year - birthday.year - 1
        else:
            user.age = date.today().year - birthday.year
        session.add(user)
        await session.commit()
        await session.refresh(user)
    return user

async def authenticate_user(email:str, password:str):
    user : User = await get_user_by_email(email)
    if not user:
        return False
    if verify_password(password=password, hashed_password=user.password):
        return user.id
    else:
        return False



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