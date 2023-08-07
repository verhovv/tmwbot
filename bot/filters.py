from aiogram.filters import BaseFilter
from aiogram.types import Message, CallbackQuery

from bot.database.models import Users
from bot.config import admin_id, channel_id, bot as main_bot


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
        return str(something.from_user.id) == admin_id


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


class ChannelFilter(BaseFilter):
    async def __call__(self, something: Message | CallbackQuery) -> bool:
        user_id = something.from_user.id
        chat_member = await main_bot.get_chat_member(chat_id=channel_id, user_id=user_id)

        if chat_member.status in ['creator', 'member']:
            return True
        channel = await main_bot.get_chat(chat_id=channel_id)

        await main_bot.send_message(chat_id=user_id, text=f'Для начала подпишитесь на канал:\n{channel.invite_link}')
