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

@pytest.mark.asyncio
async def test_check_case_1(mocker):
    mock_session = mocker.patch('user_handlers.start.AsyncSessionLocal')
    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_set_commands_users = mocker.patch('user_handlers.start.set_commands_users', new_callable=AsyncMock)

    fake_tg_user = AsyncMock(spec=types.User)
    fake_tg_user.configure_mock(id=2, username="kgkgydj")
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id=8816890796)

    fake_message = AsyncMock()
    fake_message.configure_mock( 
        from_user=fake_tg_user,
        text="/start",
        chat=fake_chat,
        answer=AsyncMock(),
        bot=AsyncMock())
    
    fake_db_user = User(user_id=2, user_name="kgkgydj", is_admin=False)
    
    fake_db = AsyncMock()
    fake_db.add = MagicMock()
    mock_select.return_value.__aenter__.return_value = fake_db
    mock_session.return_value.__aenter__.return_value = fake_db
    
    result = MagicMock()
    result.scalar_one_or_none.return_value = fake_db_user 

    fake_db.execute.return_value = result

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.configure_mock(clear = AsyncMock(), set_state = AsyncMock())

    await cmd_start(fake_message, fake_state)

    fake_db.add.assert_not_called()     
    fake_db.commit.assert_not_awaited()  

    fake_message.answer.assert_awaited_once()
    assert f"Рад видеть тебя снова, kgkgydj! Ты уже зарегистрирован." in fake_message.answer.call_args[0][0]

    mock_set_commands_users.assert_awaited_once()
    called_chat = mock_set_commands_users.call_args[0][1]
    assert called_chat == 8816890796

@pytest.mark.asyncio
async def test_check_case_2(mocker):
    mock_session = mocker.patch('user_handlers.start.AsyncSessionLocal')
    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_set_commands_users = mocker.patch('user_handlers.start.set_commands_users', new_callable=AsyncMock)
    mock_select_user = mocker.patch('user_handlers.start.select_user')
    mock_select_user.return_value = None

    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(username = "Rertet", id = 23232442, is_admin = False)
    
    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252)
    fake_message = AsyncMock()
    fake_message.configure_mock(
        from_user = fake_user,
        text = "/start", 
        chat = fake_chat,
        answer = AsyncMock(),
        bot = AsyncMock(),
        reply = AsyncMock())
    
    fake_db = AsyncMock()
    fake_db.add = MagicMock()
    mock_select.return_value = None
    mock_session.return_value.__aenter__.return_value = fake_db
    result = MagicMock()
    result.scalar_one_or_none.return_value = None
    fake_db.execute.return_value = result

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.configure_mock(clear = AsyncMock(), set_state = AsyncMock())

    await cmd_start(fake_message, fake_state)

    fake_db.add.assert_called()     
    fake_db.commit.assert_called()  

    assert "Привет, Rertet! Я успешно сохранил тебя в базу данных." in fake_message.answer.call_args[0][0]
    mock_set_commands_users.assert_awaited_once()

@pytest.mark.asyncio
async def test_check_case_3(mocker):
    mock_session = mocker.patch('user_handlers.start.AsyncSessionLocal')
    mock_select = mocker.patch('admin_tools.users_requests.AsyncSessionLocal')
    mock_set_commands_admins = mocker.patch('user_handlers.start.set_commands_admins', new_callable=AsyncMock)

    fake_user = AsyncMock(spec=types.User)
    fake_user.configure_mock(id = 131313, username = "dsdsd")

    fake_chat = AsyncMock(spec=types.Chat)
    fake_chat.configure_mock(id = 325252) 

    fake_message = AsyncMock()
    fake_message.configure_mock(
        from_user = fake_user,
        text = "/start",
        answer = AsyncMock(),
        bot = AsyncMock())

    fake_db = AsyncMock()
    fake_db_user = User(user_id=131313, user_name="dsdsd", is_admin=True)

    mock_session.return_value.__aenter__.return_value = fake_db
    mock_select.return_value.__aenter__.return_value = fake_db
    mock_result = MagicMock()
    mock_result.scalar_one_or_none.return_value = fake_db_user
    fake_db.execute.return_value = mock_result

    fake_state = AsyncMock(spec=FSMContext)
    fake_state.configure_mock(clear = AsyncMock(), set_state = AsyncMock())

    await cmd_start(fake_message, fake_state)

    fake_message.answer.assert_awaited_with("Приветствуем, Администратор dsdsd!")

    mock_set_commands_admins.assert_called_once()
    











    

    




    



    
    




    

