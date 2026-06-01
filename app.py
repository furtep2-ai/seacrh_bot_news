import aiogram
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from dotenv import load_dotenv
from aiogram.filters import Command
import os
from admin_tools.database import User, SessionLocal, Base, engine
from sqlalchemy import select 
import asyncio
from menu.base_menu import set_commands
from middlewares.check_registration import RegistrationCheckMiddleware
from handlers.start import router as router_start

load_dotenv()

token_bot = os.getenv("BOT_TOKEN")
bot = Bot(token=token_bot)
dp = Dispatcher()
dp.message.middleware(RegistrationCheckMiddleware())
dp.include_router(router_start)
            
@dp.message
async def help(message: types.Message):
    await message.answer("Отлично")

async def main():
    Base.metadata.create_all(engine)
    print("✅ Таблица 'users' успешно создана в MySQL!")
    await set_commands(bot)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

