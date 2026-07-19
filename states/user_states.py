from aiogram.fsm.state import StatesGroup, State

class BotSession(StatesGroup):
    active = State()
    blocked = State()
    admin = State()
    user = State()