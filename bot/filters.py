from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.database.models import Users
from settings import admin_ids


class UserStateFilter(BaseFilter):
    def __init__(self, state: str | list[str]):
        self.state = state

    async def __call__(self, something: Message | CallbackQuery) -> bool:
        user_state = (await Users.get(id=something.from_user.id)).state

        return user_state in self.state or user_state[:len(self.state)] == self.state


class CallbackDataFilter(BaseFilter):
    def __init__(self, callback_data: str | list[str]):
        self.callback_data = callback_data

    async def __call__(self, callback_query: CallbackQuery) -> bool:
        if isinstance(self.callback_data, str):
            return callback_query.data == self.callback_data
        elif isinstance(self.callback_data, list):
            return callback_query.data in self.callback_data


class AdminsFilter(BaseFilter):
    async def __call__(self, something: Message | CallbackQuery) -> bool:
        return something.from_user.id in admin_ids


class ButtonsFilter(BaseFilter):
    async def __call__(self, message: Message) -> bool:
        return message.text not in [
            'Запустить рекламную компанию',
            'Выполнить рекламную компанию',
            'Купить баллы', 'Продать баллы',
            'Launch an advertising campaign',
            'Run an advertising campaign',
            'Buy points', 'Sell points'
        ]
