from aiogram.filters.callback_data import CallbackData
from aiogram.fsm.state import StatesGroup, State


class AdminStates(StatesGroup):
    find_by_chaturbate_nickname = State()
    find_by_model_nickname = State()


class AdminPanelAction:
    find_by_chaturbate_nickname = 'find_by_chaturbate_nickname'
    find_by_model_nickname = 'find_by_model_nickname'


class AdminPanelCallbackFactory(CallbackData, prefix="adminpanel"):
    action: str


class EditActions:
    edit_chaturbate_nickname = 'edit_chaturbate_nickname'
    edit_model_nickname = 'edit_model_nickname'
    edit_balance = 'edit_balance'


class EditStates(StatesGroup):
    edit_chaturbate_nickname = State()
    edit_model_nickname = State()
    edit_balance = State()


class EditUserCallbackFactory(CallbackData, prefix='edituser'):
    id: int
    action: str
