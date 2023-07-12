import time

from aiogram import Router, types
from bot.database.models import Users, Tasks, TaskStorage
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

        await give_task(message.from_user.id)

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
async def on_entering_nickname_message(message: types.Message) -> None:
    user = await Users.get(id=message.from_user.id)
    user.chaturbate_nickname = message.text

    if user.lang == 'ru':
        await message.answer(text=f'Ваш ник: {user.chaturbate_nickname}')
    if user.lang == 'en':
        await message.answer(text=f'Your nickname: {user.chaturbate_nickname}')

    await user.save()

    await give_task(message.from_user.id)


async def give_task(user_id: int) -> None:
    working_tasks = await TaskStorage.filter(user_id=user_id, finished=False)
    user = await Users.get(id=user_id)
    active_tasks = await Tasks.filter(active=True)

    if len(working_tasks) == 7 or not active_tasks:
        await main_bot.send_message(chat_id=user_id, text='Нет доступных компаний')
        return

    for task in active_tasks:
        if task.working < task.max_working and task.model_nickname not in [i.model_nickname for i in working_tasks] \
                and (time.time() - task.start_time) < 30 * 60:
            await main_bot.send_message(chat_id=user_id, text=task.model_nickname)

            task.working += 1

            if task.working == 1:
                match task.time_mode:
                    case 'time1':
                        ptime = 55 * 60
                    case 'time2':
                        ptime = 115 * 60
                    case 'time3':
                        ptime = 180 * 60

                task.start_time = int(time.time())
                task.started = True
                task.end_time = task.end_time + ptime
                await main_bot.send_message(chat_id=channel_id,
                                            text=f'Началась новая рекламная компания\n\n<a href="https://t.me/{main_bot.id}">ссылка</a>')

            await task.save()

            await TaskStorage.create(task_id=task, user_id=user, model_nickname=task.model_nickname)
            return

    await main_bot.send_message(chat_id=user_id, text='Нет доступных компаний')
