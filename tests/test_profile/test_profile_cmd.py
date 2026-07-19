import pytest
from unittest.mock import AsyncMock, MagicMock
from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from user_handlers.start import cmd_start 
import pytest
from admin_tools.users_requests import delete_user, create_user
from middlewares.check_registration import RegistrationCheckMiddleware
import aiomysql
from admin_tools.database import User
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from states.user_states import BotSession
from user_handlers.profile import cmd_profile

@pytest.mark.asyncio
async def test_correct_scene(mocker):
    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(username = "Rertet", id = 23232442, is_admin = False)
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252)

    fake_message = AsyncMock()
    fake_message.configure_mock(from_user = fake_user, text = "/profile", chat = fake_chat, answer = AsyncMock(), bot = AsyncMock())

    fake_db_user = User(user_id=23232442, user_name="Rertet", is_admin=False)

    fake_db = AsyncMock()

    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_result = MagicMock()
    mock_select.return_value.__aenter__.return_value = fake_db
    mock_result.scalar_one_or_none.return_value = fake_db_user
    fake_db.execute.return_value = mock_result

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.get_state.return_value = BotSession.active.state
    fake_state.set_state = AsyncMock()

    await cmd_profile(fake_message, fake_state, fake_db_user)

    fake_message.answer.assert_awaited_with(f"Username: Rertet\n" f"ID: 23232442\n")

@pytest.mark.asyncio
async def test_not_data(mocker):
    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(username = "Rertet", id = 23232442, is_admin = False)
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252)

    fake_message = AsyncMock()
    fake_message.configure_mock(from_user = fake_user, text = "/profile", chat = fake_chat, answer = AsyncMock(), bot = AsyncMock())

    fake_db_user = None

    fake_db = AsyncMock()

    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_result = MagicMock()
    mock_select.return_value.__aenter__.return_value = fake_db
    mock_result.scalar_one_or_none.return_value = fake_db_user
    fake_db.execute.return_value = mock_result

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.get_state.return_value = BotSession.active.state
    fake_state.set_state = AsyncMock()

    await cmd_profile(fake_message, fake_state, fake_db_user)

    fake_message.answer.assert_awaited_with("Данные пользователя не найдены! Запустите бота /start")

@pytest.mark.asyncio
async def test_not_user(mocker):
    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(username = "Rertet", id = 23232442, is_admin = False)
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252)

    fake_message = AsyncMock()
    fake_message.configure_mock(from_user = fake_user, text = "/profile", chat = fake_chat, answer = AsyncMock(), bot = AsyncMock())

    fake_db = AsyncMock()

    fake_db_user = User(user_id=23232442, user_name="Rertet", is_admin=False)

    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_result = MagicMock()
    mock_select.return_value.__aenter__.return_value = fake_db
    fake_state = AsyncMock(spec=FSMContext)
    fake_state.get_state.return_value = BotSession.active.state
    fake_state.set_state = AsyncMock()
    fake_data = {"current_user": fake_db_user , "state" : fake_state}
    mock_result.scalar_one_or_none.return_value = None
    fake_db.execute.return_value = mock_result

    await cmd_profile(fake_message, fake_state, fake_db_user)

    fake_message.answer.assert_awaited_with("Что-то пошло не так!!!")





