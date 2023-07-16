import asyncio
from bot.api_client import client
from bot.database.models import *
from bot.config import time_modes, bot as main_bot
import time


async def loop_check():
    while True:
        await asyncio.sleep(5 * 60)

        started_tasks = await Tasks.filter(started=True, active=True)

        for task in started_tasks:
            active_watchers = await client.get_active_watchers(task.model_nickname)
            active_tasks_storage = await TaskStorage.filter(task=task, failed=False)

            cost = time_modes[task.time_mode][2]

            if time.time() > task.end_time:
                model = await Users.get(model_nickname=task.model_nickname)
                try:
                    if model.lang == 'ru':
                        await main_bot.send_message(chat_id=model.id, text='Рекламная компания закончена')
                    elif model.lang == 'en':
                        await main_bot.send_message(chat_id=model.id, text='The advertising campaign is over')
                except Exception:
                    pass

                task.active = False
                await task.save()

                for task_s in active_tasks_storage:
                    task_s.finished = True
                    await task_s.save()

                    user = await task_s.user.all()
                    user.balance += cost
                    await user.save()

                    try:
                        await main_bot.send_message(
                            chat_id=user.id,
                            text=f"Можете закрыть ссылку с {task_s.model_nickname}. Баланс пополнен на {cost}",
                        )
                    except Exception:
                        pass
                continue

            for task_s in active_tasks_storage:
                user = await task_s.user.all()

                if user.chaturbate_nickname in active_watchers:
                    await main_bot.send_message(
                        chat_id=user.id,
                        text=f"Вы присутствуете на стриме {task_s.model_nickname}, ваш ник: {user.chaturbate_nickname}",
                    )
                else:
                    await main_bot.send_message(
                        chat_id=user.id,
                        text=f"Вас нет на стриме {task_s.model_nickname}, ваш ник: {user.chaturbate_nickname}",
                    )
                    task_s.failed = True
                    await task_s.save()
