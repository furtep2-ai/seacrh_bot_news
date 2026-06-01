from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat
async def set_commands(bot: Bot):
    main_menu = [
        BotCommand(command="start", description="Запустить бота / Регистрация") 
    ]
    await bot.set_my_commands(commands=main_menu)

