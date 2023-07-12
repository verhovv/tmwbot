import asyncio
from api_client import client
from bot.database.models import *
from config import bot as main_bot
import time


async def loop_check():
    await asyncio.sleep(5 * 60)

    started_tasks = await Tasks.filter(started=True, active=True)

    for task in started_tasks:
        if time.time() > task.end_time:
            match task.time_mode:
                case 'time1':
                    cost = task.max_working
                case 'time2':
                    cost = task.max_working * 0.9 * 2
                case 'time3':
                    cost = task.max_working * 0.8 * 3

            task.active = False
            await task.save()

        active_watchers = await client.get_active_watchers(task.model_nickname)
        active_tasks_storage = await TaskStorage.filter(failed=False, finished=False)

        for task_s in active_tasks_storage:
            user: Users = await Users.get(id=task_s.user_id)

            if time.time() > task.end_time:
                task_s.finished = True
                await task_s.save()

                user.balance += cost
                await user.save()

                await main_bot.send_message(chat_id=task_s.user_id,
                                            text=f'Ссылку с {task_s.model_nickname} можно закрыть')
                continue

            if user.chaturbate_nickname not in active_watchers:
                task_s.failed = True
                task_s.finished = True

                await main_bot.send_message(chat_id=task_s.user_id,
                                            text=f'Вы не присутствовали на стриме у {task_s.model_nickname}. Задание больше не выполняется')
                await task_s.save()
