from aiogram import Router, types
from aiogram.filters import Command
from bot.keyboards import get_reply_keyboard

from bot.database.models import Users

router = Router()


@router.message(Command('start'))
async def on_start_cmd(message: types.Message) -> None:
    await Users.create(id=message.from_user.id)

    await message.answer(
        text='<b>Выбор языка English/ Русский</b>\n\nБот создан для взаимного пиара на сайте chaturbate',
        parse_mode='html',
        reply_markup=get_reply_keyboard([['English'], ['Русский']])
    )
