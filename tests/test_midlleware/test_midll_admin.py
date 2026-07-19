from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from middlewares.check_registration import RegistrationCheckMiddleware
import aiomysql
from admin_tools.users_requests import User
from states.user_states import BotSession
from aiogram.fsm.context import FSMContext


class Test_Midlleware_Admin():
    @pytest.mark.asyncio
    async def test_not_admin_try_use_admin(self, mocker):
        fake_db = AsyncMock()

        fake_user = AsyncMock(spec = types.User)
        fake_user.configure_mock(username = "Test", id = 45)

        mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')

        mock_select.return_value.__aenter__.return_value = fake_db

        fake_db_user = User(user_id=45, user_name="Test", is_admin=False)

        mock_result = MagicMock()
        fake_db.execute.return_value = mock_result
        mock_result.scalar_one_or_none.return_value = fake_db_user

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/list_users", answer = AsyncMock())
        
        middleware = RegistrationCheckMiddleware()
        fake_handler = AsyncMock()
        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = BotSession.active.state
        fake_state.set_state = AsyncMock()
        fake_data = {"state" : fake_state}

        await middleware(fake_handler, fake_message, fake_data)

        fake_message.answer.assert_awaited_with("🛑 У вас нет прав доступа к этой команде.")