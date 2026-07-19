from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
async def set_commands_admins(bot: Bot, chat_id: int):
    admin_menu = [
        BotCommand(command="list_users", description="Список пользователей"),
        BotCommand(command="make_admin", description="Назначить админа")
    ]
    await bot.set_my_commands(commands=admin_menu, scope=BotCommandScopeChat(chat_id=chat_id))