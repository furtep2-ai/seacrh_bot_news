from aiogram import Router, types
from aiogram.filters import Command
from admin_tools.database import User, SessionLocal, Base, engine
from sqlalchemy import select
import asyncio
from menu.admins_menu import set_commands_admins
from menu.base_menu import set_commands
from menu.users_menu import set_commands_users
router = Router()
@router.message(Command("start"))
async def cmd_start(message: types.Message):
    tg_user_name = message.from_user.username
    tg_user_id = message.from_user.id
    if not tg_user_name:
        await message.answer("⚠️ У вас не установлен username в настройках Telegram! Пожалуйста, создайте его, чтобы пользоваться ботом.")
        return
    with SessionLocal() as session:
        try:
            query = select(User).where(User.user_id == tg_user_id)
            result = session.execute(query)
            user = result.scalar_one_or_none()
            chat_id = message.chat.id
            if user is None:
                new_user = User(user_id = tg_user_id, user_name = tg_user_name)
                session.add(new_user)
                session.commit()
                await message.answer(f"Привет, {message.from_user.username}! Я успешно сохранил тебя в базу данных.")
                await set_commands_users(message.bot, chat_id)
            else:
                if user.is_admin:
                    await message.answer(f"Приветствуем, Администратор {message.from_user.username}!")
                else:
                    await message.answer(f"Рад видеть тебя снова, {message.from_user.username}! Ты уже зарегистрирован.")
                    await set_commands_users(message.bot, chat_id)
        except Exception as e:
            await message.reply(f"Упс, что-то пошло не так... Ошибка: {e}")