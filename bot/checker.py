import asyncio
from bot.api_client import client
from bot.database.models import *
from bot.config import bot as main_bot
import time


async def loop_check():
    print("start loop")
    while True:
        await asyncio.sleep(3 * 7)

        started_tasks = await Tasks.filter(active=True)
        print(started_tasks)
        for task in started_tasks:
            print(task)
            if time.time() > task.end_time:
                match task.time_mode:
                    case "time1":
                        cost = task.max_working
                    case "time2":
                        cost = task.max_working * 0.9 * 2
                    case "time3":
                        cost = task.max_working * 0.8 * 3

                # task.active = False
                # await task.save()

            active_watchers = await client.get_active_watchers(task.model_nickname)
            active_tasks_storage = await TaskStorage.filter(task_id=task)

            for task_s in active_tasks_storage:
                user = await task_s.user_id.all()
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
                # if time.time() > task.end_time:
                #     task_s.finished = True
                #     await task_s.save()

                #     user.balance += cost
                #     await user.save()

                #     await main_bot.send_message(
                #         chat_id=task_s.user_id,
                #         text=f"Ссылку с {task_s.model_nickname} можно закрыть",
                #     )
                #     continue

                # if user.chaturbate_nickname not in active_watchers:
                #     task_s.failed = True
                #     task_s.finished = True

                #     await main_bot.send_message(
                #         chat_id=task_s.user_id,
                #         text=f"Вы не присутствовали на стриме у {task_s.model_nickname}. Задание больше не выполняется",
                #     )
                #     await task_s.save()
