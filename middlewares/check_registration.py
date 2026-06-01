from aiogram import BaseMiddleware
from aiogram.types import Message
from typing import Any, Dict, Awaitable, Callable
from admin_tools.database import SessionLocal, User
from sqlalchemy import select
class RegistrationCheckMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: Dict[str, Any]
    ) -> Any:
        if event.text and event.text.startswith("/start"):
            return await handler(event, data)
        with SessionLocal() as session:
            user_id = event.from_user.id
            if user_id:
                query = select(User).where(User.user_id == user_id)
                result = session.execute(query)
                user = result.scalar_one_or_none()
                if user:
                    return await handler(event, data)
        await event.answer("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")
        return 
        
        
        
        
                
                
                


        