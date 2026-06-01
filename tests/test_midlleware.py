from unittest.mock import AsyncMock, MagicMock, patch
from aiogram import types
import pytest
from middlewares.check_registration import RegistrationCheckMiddleware
@pytest.mark.asyncio
async def test_check_midlleware_not_login():
    fake_user = MagicMock(spec=types.User)
    fake_user.username = "TestUser"
    fake_user.id = 345

    fake_message = AsyncMock()
    fake_message.from_user = fake_user
    fake_message.text = "/help"
    fake_message.chat = 232

    fake_message.answer = AsyncMock()
    fake_message.reply = AsyncMock()
    fake_message.bot = AsyncMock()

    middleware = RegistrationCheckMiddleware()
    fake_handler = AsyncMock()
    fake_data = {}

    await middleware(handler=fake_handler, event=fake_message, data=fake_data)

    fake_message.answer.assert_called_with("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")

@pytest.mark.asyncio
async def test_check_midlleware_login():
    fake_user = MagicMock(spec=types.User)
    fake_user.username = "TestUser"
    fake_user.id = 2

    fake_message = AsyncMock()
    fake_message.from_user = fake_user
    fake_message.text = "/help"
    fake_message.chat = 232

    fake_message.answer = AsyncMock()
    fake_message.reply = AsyncMock()
    fake_message.bot = AsyncMock()

    middleware = RegistrationCheckMiddleware()
    fake_handler = AsyncMock()
    fake_data = {}

    await middleware(handler=fake_handler, event=fake_message, data=fake_data)

    fake_message.answer.assert_not_called()

@pytest.mark.asyncio
@patch('middlewares.check_registration.SessionLocal')
async def test_check_midlleware_start(mock_session):
    fake_user = MagicMock(spec = types.User)
    fake_user.username = "Test"
    fake_user.id = 45

    fake_message = AsyncMock()
    fake_message.from_user = fake_user
    fake_message.text = "/start"

    fake_message.answer = AsyncMock()

    middleware = RegistrationCheckMiddleware()
    fake_handler = AsyncMock()
    fake_data = {}

    await middleware(fake_handler, fake_message, fake_data)

    mock_session.assert_not_called()

@pytest.mark.asyncio
@patch('middlewares.check_registration.SessionLocal')
async def test_check_midlleware_start_invalid_type(mock_session):
    fake_db = MagicMock()
    mock_session.return_value.__enter__.return_value = fake_db
    fake_db.execute.return_value.scalar_one_or_none.return_value = None
    fake_user = MagicMock(spec = types.User)
    fake_user.username = "Test"
    fake_user.id = 45

    fake_message = AsyncMock()
    fake_message.from_user = fake_user
    fake_message.text = None

    fake_message.answer = AsyncMock()
    middleware = RegistrationCheckMiddleware()
    fake_handler = AsyncMock()
    fake_data = {}

    await middleware(fake_handler, fake_message, fake_data)

    fake_message.answer.assert_called_with("Пожалуйста, введите команду /start, чтобы пройти регистрацию.")
