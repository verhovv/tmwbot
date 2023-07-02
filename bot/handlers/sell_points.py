from aiogram import Router, types
from aiogram.filters import Text

from bot.database.models import Users
from bot.filters import UserStateFilter, CallbackDataFilter, ButtonsFilter
from bot.keyboards import get_inline_keyboard
from bot.settings import admin_ids, bot as main_bot

router = Router()


@router.message(Text(['Продать баллы', 'Sell points']))
async def on_sell_points_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    if user.lang == 'ru':
        await message.answer('Введите количесвто (от 100)')
    if user.lang == 'en':
        await message.answer('Enter the quantity (from 100)')

    user.state = 'selling points'
    await user.save()


@router.message(UserStateFilter('selling points'))
async def on_points_amount_message(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    try:
        points_amount = int(message.text)
    except ValueError:
        if user.lang == 'ru':
            await message.answer('Недопустимое значени')
        elif user.lang == 'en':
            await message.answer('Invalid value')

        return

    if user.balance < points_amount:
        if user.lang == 'ru':
            await message.answer('У Вас недолстаточно баллов')
        elif user.lang == 'en':
            await message.answer('You don\'t have enough points')
        return

    if points_amount < 100:
        if user.lang == 'ru':
            await message.answer('Купить можно только от 100 баллов')
        elif user.lang == 'en':
            await message.answer('You can only buy from 100 points')
        return

    if user.lang == 'ru':
        await message.answer(text='Введите кошелек usdt trc-20 либо номер qiwi кошелька')
    elif user.lang == 'en':
        await message.answer(text='Enter the usdt trc-20 wallet or the qiwi wallet number')

    user.state = f'entering wallet {points_amount}'
    await user.save()


@router.message(UserStateFilter('entering wallet'), ButtonsFilter())
async def on_wallet_message(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    *_, points_to_sell = user.state.split()
    points_to_sell = int(points_to_sell)

    if user.lang == 'ru':
        text = 'Заявки обрабатываются в ручном режиме в рабочее время администратора (10-20 ч.  МСК)\n' \
               f'Ваш виртуальный кошелек: {message.text}. Баллы для продажи: {points_to_sell}'
        keyboard = get_inline_keyboard([
            [{'Подтвердить': 'confirm'}]
        ])
    elif user.lang == 'en':
        text = 'Applications are processed manually during the administrator\'s working hours (10-20 hours Moscow time)\n' \
               f'Your virtual wallet: {message.text}. Points to sell: {points_to_sell}'
        keyboard = get_inline_keyboard([
            [{'Confirm': 'confirm'}]
        ])
    await message.answer(text=text, reply_markup=keyboard)


@router.callback_query(CallbackDataFilter('confirm'))
async def on_wallet_message(callback_query: types.CallbackQuery) -> None:
    user = await Users.get(id=callback_query.from_user.id)

    if user.lang == 'ru':
        text = 'Отправлено на проверку'
    elif user.lang == 'en':
        text = 'Sent for verification'

    await callback_query.message.edit_text(text=text, reply_markup=None)

    points = int(callback_query.message.text.split()[-1])

    for admin_id in admin_ids:
        await main_bot.send_message(chat_id=admin_id,
                                    text=callback_query.from_user.mention_html() \
                                         + '\nwallet: ' +
                                         callback_query.message.text.split('wallet: ')[1].split('.Total')[0] \
                                         + '\npoints:' + str(points),
                                    parse_mode='html'
                                    )

    user.balance -= points
    await user.save()
