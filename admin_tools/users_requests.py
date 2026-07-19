from admin_tools.database import AsyncSessionLocal, User
from sqlalchemy import delete, insert, select
import asyncio
import aiomysql

async def delete_user(user_id: int):
    async with AsyncSessionLocal() as session:
        query = delete(User).where(User.user_id == user_id)
        result = await session.execute(query)
        await session.commit()
        return True if result.rowcount>0 else False
    
async def create_user(user_id: int, user_name: str, is_admin: bool):
    async with AsyncSessionLocal() as session:
        query = insert(User).values(
        user_id=user_id,
        user_name=user_name,
        is_admin=is_admin)
        result = await session.execute(query)
        await session.commit()
        return True if result.rowcount>0 else False
    
async def list_users():
    async with AsyncSessionLocal() as session:
        query = select(User)
        result = await session.execute(query)
        users = result.scalars().all()
        return users if users else False
    
async def select_user(user_id: int):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
    return user if user else None

async def make_admin(user_id: int, number: int):
    async with AsyncSessionLocal() as session:
        query = select(User).where(User.user_id == user_id)
        result = await session.execute(query)
        user = result.scalar_one_or_none()

        if user:
            if number == 1 or number == 0:
                user.is_admin = number
                await session.commit()
                return True
        return None


    


