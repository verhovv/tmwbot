from aiogram import Router
from aiogram import types
from aiogram.filters import Text

from bot.filters import UserStateFilter, CallbackDataFilter, ButtonsFilter
from bot.database.models import Users

router = Router()


@router.message(Text(['Buy points', 'Купить баллы']))
async def on_buy_points_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    user.state = 'buying points'
    await user.save()

    if user.lang == 'ru':
        text = 'Введите количество (от 10 баллов)'
    elif user.lang == 'en':
        text = 'Enter the amount (from 10 points)'

    await message.answer(text=text)


@router.message(UserStateFilter('buying points'), ButtonsFilter())
async def on_points_amount_message(message: types.Message):
    user = await Users.get(id=message.from_user.id)

    try:
        points_amount = int(message.text)
    except ValueError:
        if user.lang == 'ru':
            await message.answer('Недопустимое значени')
        elif user.lang == 'en':
            await message.answer('Invalid value')

        return

    if points_amount < 10:
        if user.lang == 'ru':
            await message.answer('Купить можно только от 10 баллов')
        elif user.lang == 'en':
            await message.answer('You can only buy from 10 points')
        return

    if user.lang == 'ru':
        await message.answer(text=f'{points_amount} балл(ов). Стоимость: {0.4 * points_amount}$')
    elif user.lang == 'en':
        await message.answer(text=f'{points_amount} points. Cost: {0.4 * points_amount}$')

    await message.answer(text='Далее идет платежная система')
