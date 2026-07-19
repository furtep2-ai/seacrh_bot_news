from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from admin_tools.users_requests import User
from states.admin_states import AdminStates
from aiogram.fsm.context import FSMContext
from admin_handlers.make_admin import make_admin_cmd

class Test_Make_Admin():
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

        await make_admin_cmd(fake_message, fake_state, fake_db_user)

        fake_message.answer.assert_awaited_with("Введите ID пользователя, которого хотите назначить админом.")

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

        await make_admin_cmd(fake_message, fake_state, fake_db_user)

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

        await make_admin_cmd(fake_message, fake_state, fake_db_user)

        fake_message.answer.assert_awaited_with("У вас нет прав")




