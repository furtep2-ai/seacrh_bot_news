from aiogram import Router, types
from aiogram.filters import Command
from admin_tools.database import User, AsyncSessionLocal, Base, engine
from sqlalchemy import select
import asyncio
from menu.admins_menu import set_commands_admins
from menu.base_menu import set_commands
from menu.users_menu import set_commands_users
router = Router()
import aiomysql
from aiogram.fsm.context import FSMContext
from states.user_states import BotSession
from admin_tools.users_requests import select_user

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    await state.clear()
    tg_user_name = message.from_user.username
    tg_user_id = message.from_user.id
    if not tg_user_name:
        await message.answer("⚠️ У вас не установлен username в настройках Telegram! Пожалуйста, создайте его, чтобы пользоваться ботом.")
        return
    user = await select_user(tg_user_id)
    chat_id = message.chat.id
    if user is None:
        async with AsyncSessionLocal() as session:
            new_user = User(user_id = tg_user_id, user_name = tg_user_name)
            session.add(new_user)
            await session.commit()
        await state.set_state(BotSession.active)
        await message.answer(f"Привет, {message.from_user.username}! Я успешно сохранил тебя в базу данных.")
        await set_commands_users(message.bot, chat_id)
    else:
        if user.is_admin:
            await state.set_state(BotSession.active)
            await message.answer(f"Приветствуем, Администратор {message.from_user.username}!")
            await set_commands_admins(message.bot, chat_id)
        else:
            await state.set_state(BotSession.active)
            await message.answer(f"Рад видеть тебя снова, {message.from_user.username}! Ты уже зарегистрирован.")
            await set_commands_users(message.bot, chat_id)
        