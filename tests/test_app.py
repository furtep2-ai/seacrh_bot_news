from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
from handlers.start import cmd_start 
import pytest
from admin_tools.users_requests import delete_user, create_user
from middlewares.check_registration import RegistrationCheckMiddleware

@pytest.mark.asyncio
@patch('handlers.start.set_commands_users', new_callable=AsyncMock)
async def test_check_case_1(mock_set_commands_users):
    fake_user = MagicMock(spec=types.User)
    fake_user.username = "kgkgydj"
    fake_user.id = 2

    fake_message = AsyncMock(spec=types.Message)
    fake_message.from_user = fake_user
    fake_message.text = "/start"
    fake_message.chat = MagicMock(spec=types.Chat)
    fake_message.chat.id = 8816890796

    fake_message.answer = AsyncMock()
    fake_message.reply = AsyncMock()
    fake_message.bot = AsyncMock()

    await cmd_start(fake_message)

    fake_message.answer.assert_called_once()

    called_text = fake_message.answer.call_args.args[0]

    mock_set_commands_users.assert_called_once()

    called_bot = mock_set_commands_users.call_args.args[0]
    called_chat = mock_set_commands_users.call_args.args[1]
    assert called_chat == 8816890796

@pytest.mark.asyncio
@patch('handlers.start.set_commands_users', new_callable=AsyncMock)
async def test_check_case_2(mock_set_commands_users):
    fake_user = MagicMock(spec=types.User)
    fake_user.username = "Rertet"
    fake_user.id = 23232442
    
    fake_message = AsyncMock()
    fake_message.from_user = fake_user
    fake_message.text = "/start"
    fake_message.chat = MagicMock(spec=types.Chat)
    fake_message.chat.id = 325252

    fake_message.answer = AsyncMock()
    fake_message.reply = AsyncMock()
    fake_message.bot = AsyncMock()

    await cmd_start(fake_message)

    fake_message.answer.assert_called_with("Привет, Rertet! Я успешно сохранил тебя в базу данных.")

    mock_set_commands_users.assert_called_once()

    assert delete_user(23232442) == True

@pytest.mark.asyncio
async def test_check_case_3():
    try:
        delete = False
        assert create_user(131313, "dsdsd", True) == True
        delete = True
        fake_user = MagicMock(spec=types.User)
        fake_user.username = "dsdsd"
        fake_user.id = 131313
            
        fake_message = AsyncMock()
        fake_message.from_user = fake_user
        fake_message.text = "/start"
        fake_message.chat = MagicMock(spec=types.Chat)
        fake_message.chat.id = 325252

        fake_message.answer = AsyncMock()
        fake_message.reply = AsyncMock()
        fake_message.bot = AsyncMock()

        await cmd_start(fake_message)

        fake_message.answer.assert_called_with("Приветствуем, Администратор dsdsd!")
    finally:
        if delete:
            assert delete_user(131313) == True











    

    




    



    
    




    

