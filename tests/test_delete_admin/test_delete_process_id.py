from admin_handlers.delete_admin import delete_process_id_user
from aiogram import types
from unittest.mock import AsyncMock, MagicMock
from aiogram.fsm.context import FSMContext
from admin_tools.users_requests import User
import pytest
from states.admin_states import AdminStates

class Test_process_id():
    @pytest.mark.asyncio
    async def test_case_not_admin(self):
        fake_user = AsyncMock(spec = types.User)
        fake_user.configure_mock(username = "Test", id = 45)

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/make_admin", answer = AsyncMock())

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = None
        fake_state.set_state = AsyncMock()

        fake_db_user = User(user_id=45, user_name="Test", is_admin=False)

        await delete_process_id_user(fake_message, fake_state , fake_db_user)

        fake_message.answer.assert_awaited_with("У вас нет прав для выполнения этой команды.")

    @pytest.mark.asyncio
    async def test_case_not_user(self):
        fake_user = AsyncMock(spec = types.User)
        fake_user.configure_mock(username = "Test", id = 45)

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/make_admin", answer = AsyncMock())

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = None
        fake_state.set_state = AsyncMock()

        fake_db_user = None 

        await delete_process_id_user(fake_message, fake_state , fake_db_user)

        fake_message.answer.assert_awaited_with("У вас нет прав для выполнения этой команды.")