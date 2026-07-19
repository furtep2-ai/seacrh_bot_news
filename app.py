import aiogram
from aiogram import Bot, Dispatcher, types, BaseMiddleware
from dotenv import load_dotenv
from aiogram.filters import Command
import os
from admin_tools.database import User, AsyncSessionLocal, Base, engine
import asyncio
from menu.base_menu import set_commands
from middlewares.check_registration import RegistrationCheckMiddleware
from user_handlers.start import router as start_router
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from middlewares.timer import TimeoutMenuMiddleware
import pytz
from admin_handlers.list_users_func import router as list_router
import aiomysql
from user_handlers.profile import router as profile_router
from admin_handlers.make_admin import router as make_admin_router
load_dotenv()

token_bot = os.getenv("BOT_TOKEN")
bot = Bot(token=token_bot)
dp = Dispatcher()
         
@dp.message(Command("help"))
async def help(message: types.Message):
    await message.answer("Отлично")

async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    dp.message.middleware(RegistrationCheckMiddleware())
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Almaty"))
    scheduler.start()
    dp.message.middleware(TimeoutMenuMiddleware(scheduler))
    print("✅ Таблица 'users' успешно создана в MySQL!")
    await set_commands(bot)
    dp.include_router(start_router)
    dp.include_router(list_router)
    dp.include_router(profile_router)
    dp.include_router(make_admin_router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    print("Бот готов к запуску")
    asyncio.run(main())
    

