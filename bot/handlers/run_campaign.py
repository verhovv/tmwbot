from aiogram import Router, types
from bot.database.models import Users
from bot.filters import *
from aiogram.filters import Text

router = Router()


@router.message(Text(['Выполнить рекламную компанию', 'Run an advertising campaign']))
async def on_run_campaign_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    if user.chaturbate_nickname:
        if user.lang == 'ru':
            await message.answer(text=f'Ваш ник: {user.chaturbate_nickname}')
        if user.lang == 'en':
            await message.answer(text=f'Your nickname: {user.chaturbate_nickname}')

        return

    if user.lang == 'ru':
        await message.answer(
            text='Введите ник пользователя Chaturbate\n\n(возможен выполнение до 7 рекламных компаний на одном сайте одновременно)')
    elif user.lang == 'en':
        await message.answer(
            text='Enter the user\'s nickname Chaturbate\n\n (it is possible to run up to 7 advertising campaigns on one site at the same time)')

    user.state = 'entering chaturbate name'

    await user.save()


@router.message(UserStateFilter('entering chaturbate name'), ButtonsFilter())
async def on_entering_nickname_message(message: types.Message):
    user = await Users.get(id=message.from_user.id)
    user.chaturbate_nickname = message.text

    if user.lang == 'ru':
        await message.answer(text=f'Ваш ник: {user.chaturbate_nickname}')
    if user.lang == 'en':
        await message.answer(text=f'Your nickname: {user.chaturbate_nickname}')

    await user.save()
