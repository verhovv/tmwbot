from aiogram import types, Router, F
from aiogram.filters import Text

from bot.database.models import Users
from bot import keyboards

from bot.filters import CallbackDataFilter, UserStateFilter, ButtonsFilter

router = Router()


@router.message(Text(['Launch an advertising campaign', 'Запустить рекламную компанию']))
async def on_launch_campaign_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    if user.lang == 'ru':
        text = '<b>55-70 мин</b>\n1 пользователь - 1 балл\n\n<b>115-140 мин</b>\n1 пользователь 0,9 балла в час\n\n<b>180-200 мин</b>\n1 пользователь 0,8 балла в час'
        keyboard = keyboards.get_inline_keyboard([
            [{'55-70 мин': 'time1'}],
            [{'115-140 мин': 'time2'}],
            [{'180-200 мин': 'time3'}]]
        )
    elif user.lang == 'en':
        text = '<b>55-70 min</b>\n1 user - 1 point\n\n<b>115-140 min</b>\n1 user 0.9 points per hour\n\n<b>180-200 min</b>\n1 user 0.8 points per hour'
        keyboard = keyboards.get_inline_keyboard([
            [{'55-70 min': 'time1'}],
            [{'115-140 min': 'time2'}],
            [{'180-200 min': 'time3'}]]
        )

    await message.answer(text=text, reply_markup=keyboard, parse_mode='html')


@router.callback_query(CallbackDataFilter(['time1', 'time2', 'time3']))
async def on_time_callback(callback_query: types.CallbackQuery) -> None:
    user = await Users.get(id=callback_query.from_user.id)

    if user.lang == 'ru':
        text = 'Введите количество пользователей'
    elif user.lang == 'en':
        text = 'Enter the number of users'

    user.state = f'{callback_query.data} entering'
    await user.save()


@router.message(UserStateFilter([f'{x} entering' for x in ['time1', 'time2', 'time3']]), ButtonsFilter())
async def on_user_count_entering(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    mode, _ = user.state.split()
