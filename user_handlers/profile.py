from aiogram import Router, types
from aiogram.filters import Command
from admin_tools.database import User, AsyncSessionLocal, Base, engine
from admin_tools.users_requests import select_user
import asyncio
router = Router()
import aiomysql
from aiogram.fsm.context import FSMContext
from states.user_states import BotSession

@router.message(Command("profile"))
async def cmd_profile(message: types.Message, state: FSMContext, current_user: User = None):
    if not current_user:
        await message.answer("Данные пользователя не найдены! Запустите бота /start")
        return 
    user_id = current_user.user_id
    user = await select_user(user_id)
    if user:
        await message.answer(
        f"Username: {user.user_name}\n"
        f"ID: {user.user_id}\n")
        return
    else:
        await message.answer("Что-то пошло не так!!!")

