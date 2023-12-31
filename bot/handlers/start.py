from aiogram import Router, types
from aiogram.filters import Command

from bot.config import admin_id
from bot.filters import AdminsFilter
from bot.keyboards import get_reply_keyboard

from bot.database.models import Users

router = Router()


@router.message(Command('start'))
async def on_start_cmd(message: types.Message) -> None:
    try:
        await Users.create(id=message.from_user.id)
    except Exception:
        pass

    await message.answer(
        text='<b>Выбор языка English / Русский</b>\n\nБот создан для взаимного пиара на сайте chaturbate',
        parse_mode='html',
        reply_markup=get_reply_keyboard([['English'], ['Русский']])
    )


@router.message(Command('admin'), AdminsFilter())
async def on_start_cmd(message: types.Message) -> None:
    await message.answer(
        text='Ваши возможности админа',
        reply_markup=get_reply_keyboard([['Админ панель'], ['Администрирование заданий'], ['Статистика']])
    )
