import time

from aiogram import types, Router
from aiogram.filters import Text

from bot.database.models import Users, Tasks
from bot import keyboards
from bot.config import channel_id, time_modes, bot as main_bot
from bot.filters import CallbackDataFilter, UserStateFilter, ButtonsFilter

router = Router()

TASK1_TIME = 55 * 60
TASK2_TIME = 115 * 60
TASK3_TIME = 180 * 60


@router.message(
    Text(["Launch an advertising campaign", "Запустить рекламную компанию"])
)
async def on_launch_campaign_btn(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    if user.lang == "ru":
        text = f"<b>55-70 мин</b>\n1 пользователь - 1 балл\n\n<b>115-140 мин</b>\n1 пользователь 0,9 балла в час\n\n<b>180-200 мин</b>\n1 пользователь 0,8 балла в час\n\nБаланс: {user.balance:.2f}"
        keyboard = keyboards.get_inline_keyboard(
            [
                [{"55-70 мин": "time1"}],
                [{"115-140 мин": "time2"}],
                [{"180-200 мин": "time3"}],
            ]
        )
    elif user.lang == "en":
        text = f"<b>55-70 min</b>\n1 user - 1 point\n\n<b>115-140 min</b>\n1 user 0.9 points per hour\n\n<b>180-200 min</b>\n1 user 0.8 points per hour\n\nBalance: {user.balance:.2f}"
        keyboard = keyboards.get_inline_keyboard(
            [
                [{"55-70 min": "time1"}],
                [{"115-140 min": "time2"}],
                [{"180-200 min": "time3"}],
            ]
        )

    await message.answer(text=text, reply_markup=keyboard, parse_mode="html")


@router.callback_query(CallbackDataFilter(["time1", "time2", "time3"]))
async def on_time_callback(callback_query: types.CallbackQuery) -> None:
    user = await Users.get(id=callback_query.from_user.id)

    if user.lang == "ru":
        text = "Введите количество пользователей\nВремя выполнения начнет считаться от 10 человек начавших выполнять ваше задание"
    elif user.lang == "en":
        text = "Enter the number of users\nThe completion time will start counting from 10 people who have started to complete your task"

    await callback_query.message.answer(text=text)

    user.state = f"{callback_query.data} entering"
    await user.save()

    await callback_query.answer()


@router.message(
    UserStateFilter([f"{x} entering" for x in ["time1", "time2", "time3"]]),
    ButtonsFilter(),
)
async def on_user_count_entering(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)

    mode, _ = user.state.split()

    try:
        users_count = int(message.text)
    except ValueError:
        if user.lang == "ru":
            await message.answer(text="Недопустимое значение")
        elif user.lang == "en":
            await message.answer(text="Invalid value")
        return

    if users_count < 10:
        if user.lang == "ru":
            await message.answer(text="Допускаются значения от 10")
        elif user.lang == "en":
            await message.answer(text="Values from 10 are allowed")
        return
    cost = users_count * time_modes[mode][2]
    if user.balance < cost:
        if user.lang == "ru":
            await message.answer(text="У вас недостаточно баллов")
        elif user.lang == "en":
            await message.answer(text="You don't have enough funds")
        return

    if user.model_nickname:
        if user.lang == 'ru':
            await message.answer(
                text=f'Ник: {user.model_nickname}\nВремя выполнения: {time_modes[mode][0]}\nЦена: {time_modes[mode][2]} за пользователя | (всего {time_modes[mode][2] * users_count})',
                reply_markup=keyboards.get_inline_keyboard([
                    [{'Подтвердить': f'ct {users_count} {mode}'}]
                ]))
        elif user.lang == 'en':
            await message.answer(
                text=f'Nickname: {user.model_nickname}\nLead time: {time_modes[mode][0]}\nCost: {time_modes[mode][2]} per user | (at all {time_modes[mode][2] * users_count})',
                reply_markup=keyboards.get_inline_keyboard([
                    [{'Confirm': f'ct {users_count} {mode}'}]
                ])
            )
    else:
        user.state = f"entering model name {mode} {users_count}"
        if user.lang == "ru":
            await message.answer(text="Введите ник модели")
        elif user.lang == "en":
            await message.answer(text="Enter the model's nickname")

    user.balance -= cost
    await user.save()


@router.message(UserStateFilter("entering model name"), ButtonsFilter())
async def on_model_name_message(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    *_, mode, users_count = user.state.split()
    users_count = int(users_count)

    user.model_nickname = message.text
    user.state = "new"
    await user.save()

    if user.lang == 'ru':
        await message.answer(
            text=f'Ник: {user.model_nickname}\nВремя выполнения: {time_modes[mode][0]}\nЦена: {time_modes[mode][2]} за пользователя | (всего {time_modes[mode][2] * users_count})',
            reply_markup=keyboards.get_inline_keyboard([
                [{'Подтвердить': f'ct {users_count} {mode}'}]
            ]))
    elif user.lang == 'en':
        await message.answer(
            text=f'Nickname: {user.model_nickname}\nLead time: {time_modes[mode][0]}\nCost: {time_modes[mode][2]} per user | (at all {time_modes[mode][2] * users_count})',
            reply_markup=keyboards.get_inline_keyboard([
                [{'Confirm': f'ct {users_count} {mode}'}]
            ])
        )


@router.callback_query(lambda x: x.data.split()[0] == 'ct')
async def on_ct_callback(callback_query: types.CallbackQuery):
    _, user_count, mode = callback_query.data.split()
    user_count = int(user_count)

    user = await Users.get(id=callback_query.from_user.id)

    await Tasks.create(
        time_mode=mode,
        max_working=user_count,
        user=user,
        start_time=int(time.time()),
        coins_after_ending=user.balance
    )

    await callback_query.message.edit_reply_markup(None)

    if user.lang == 'ru':
        await callback_query.message.answer(text='Рекламная компания началась')
    elif user.lang == 'en':
        await callback_query.message.answer(text='Advertising campaign started')

    await write_about_new_campaign()

    await callback_query.answer()


async def write_about_new_campaign():
    await main_bot.send_message(
        chat_id=channel_id,
        text="Началась новая рекламная компания\n\n"
             f'<a href="tg://user?id={main_bot.id}">Ссылка на бота</a>',
    )
