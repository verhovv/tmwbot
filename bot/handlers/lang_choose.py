from aiogram import Router
from aiogram import types
from bot.keyboards import get_reply_keyboard
from bot.database.models import Users
from aiogram.filters import Text

router = Router()


@router.message(Text('English'))
async def on_english_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    user.lang = 'en'
    await user.save()

    await message.answer(
        text='Language selected',
        reply_markup=get_reply_keyboard([
            ['Launch an advertising campaign'],
            ['Run an advertising campaign'],
            ['Buy points'],
            ['Sell points']
        ])
    )


@router.message(Text('Русский'))
async def on_english_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    user.lang = 'ru'
    await user.save()

    await message.answer(
        text='Язык выбран',
        reply_markup=get_reply_keyboard([
            ['Запустить рекламную компанию'],
            ['Выполнить рекламную компанию'],
            ['Купить баллы'],
            ['Продать баллы']
        ])
    )
