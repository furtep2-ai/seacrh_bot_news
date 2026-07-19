from admin_handlers.delete_admin import delete_admin_cmd
from aiogram import types
from unittest.mock import AsyncMock, MagicMock
from aiogram.fsm.context import FSMContext
from admin_tools.users_requests import User
import pytest
from states.admin_states import AdminStates

class Test_Delete_Admin():
    @pytest.mark.asyncio
    async def test_case_correct(self):
        fake_user = AsyncMock(spec = types.User)
        fake_user.configure_mock(username = "Test", id = 45)

        fake_message = AsyncMock()
        fake_message.configure_mock(from_user = fake_user, text = "/make_admin", answer = AsyncMock())

        fake_state = AsyncMock(spec=FSMContext)
        fake_state.get_state.return_value = None
        fake_state.set_state = AsyncMock()

        fake_db_user = User(user_id=45, user_name="Test", is_admin=True)

        await delete_admin_cmd(fake_message, fake_state, fake_db_user)

        fake_message.answer.assert_awaited_with('Введите ID пользователя, которого хотите лишить админских прав.')

        fake_state.set_state.assert_called_with(AdminStates.waiting_for_user_id)

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

        await delete_admin_cmd(fake_message, fake_state, fake_db_user)

        fake_message.answer.assert_awaited_with("Ошибка: данные пользователя не найдены.")

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

        await delete_admin_cmd(fake_message, fake_state, fake_db_user)

        fake_message.answer.assert_awaited_with("У вас нет прав")

    

    
