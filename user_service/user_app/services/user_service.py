from user_app.models.database import engine, Base, new_session, Profile
import pydantic
from sqlalchemy.future import select
from datetime import date

async def drop_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

async def no_info_user(email:str):
    async with new_session() as session:
        stmt  = select(Profile).where((Profile.email == email))
        result = await session.execute(stmt)
        user : Profile = result.scalars().first()
        if any(not field for field in [user.name, user.nickname, user.last_name, user.age]):
            return True
        else:
            return False

async def add_user(name:str, last_name:str, birthday:date, user_id : int):
    async with new_session() as session:
        if (date.today().month, date.today().day) < (birthday.month, birthday.day):
            age = date.today().year - birthday.year - 1
        else:
            age = date.today().year - birthday.year

        new_user : Profile = (await session.execute(select(Profile).where((Profile.user_id == user_id)))).scalars().first()
        if not new_user:
            new_user = Profile(name=name, last_name=last_name, user_id=user_id, age=age)
            session.add(new_user)
        else:
            new_user.name = name
            new_user.last_name = last_name
            new_user.birthday = birthday
        await session.commit()
        await session.refresh(new_user)
    return new_user

async def get_profile(user_id):
    async with new_session() as session:
        try:
            user = (await session.execute(select(Profile).where((Profile.user_id == user_id)))).scalars().first()
        except ValueError as e:
            return None
        return user.id