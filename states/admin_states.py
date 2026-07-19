from aiogram.fsm.state import StatesGroup, State

class AdminStates(StatesGroup):
    admin_active = State()
    waiting_for_user_id = State()