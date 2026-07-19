from aiogram import Router, types
from aiogram.types import BotCommand
from aiogram.filters import Command
from menu.admins_menu import set_commands_admins
from admin_tools.database import AsyncSessionLocal, User
from sqlalchemy import select
import aiomysql
from aiogram.fsm.context import FSMContext
from admin_tools.users_requests import list_users


router = Router()

@router.message(Command("list_users"))
async def list_users_cmd(message: types.Message, state: FSMContext, current_user: User = None):
    if not current_user:
        await message.answer("Данные пользователя не найдены! Запустите бота /start")
        return 
    if current_user.is_admin:
        result = await list_users()
        if result:
            response_text = "👥 **Список пользователей:**\n\n"
            for i in result:
                response_text += f"• ID: `{i.user_id}` | Имя: `{i.user_name}` | Админ: {'1' if i.is_admin else '0'}\n"
            await message.answer(response_text)
        else:
            await message.answer("Список пользователей отсуствует")
    else:
        await message.answer("У вас нету доступа")
                
            

