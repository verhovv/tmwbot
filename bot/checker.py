import asyncio
from bot.api_client import client
from bot.database.models import *
from bot.config import time_modes, bot as main_bot
import time


async def loop_check():
    while True:
        await asyncio.sleep(60)
        active_tasks_storage = await TaskStorage.filter(failed=False, finished=False)
        for active_task in active_tasks_storage:
            task = await active_task.task.get()

            user = await active_task.user.get()
            active_watchers = await client.get_active_watchers(user.model_nickname)
            if user.chaturbate_nickname in active_watchers:
                await main_bot.send_message(
                    chat_id=user.id,
                    text=f"Вы присутствуете на стриме {user.model_nickname}, ваш ник: {user.chaturbate_nickname}",
                )
            else:
                await main_bot.send_message(
                    chat_id=user.id,
                    text=f"Вас нет на стриме {user.model_nickname}, ваш ник: {user.chaturbate_nickname}.\n"
                         f"Можете закрыть ссылку, Ваш баланс не изменился.",
                )
                task.working -= 1
                await task.save()

                active_task.failed = True
                active_task.finished = True
                await active_task.save()
                continue

            task = await active_task.task.get()
            time_to_end = active_task.start_time + time_modes[task.time_mode][1]

            if time_to_end < time.time():
                cost = time_modes[task.time_mode][2]
                active_task.finished = True

                user = await active_task.user.get()
                user.balance += cost

                await user.save()
                await active_task.save()

                await main_bot.send_message(
                    chat_id=user.id,
                    text=f"Можете закрыть ссылку с {user.model_nickname}. Баланс пополнен на {cost}",
                )

        for model_task in await Tasks.filter(active=True):
            cost = time_modes[model_task.time_mode][2]
            model_task_storage = await TaskStorage.filter(failed=False, finished=False, task=model_task)
            if model_task.start_time + 5 * 60 < time.time() and model_task.working < 10:
                model_user = await model_task.user.get()
                await main_bot.send_message(
                    chat_id=model_user.id,
                    text=f"Ваша рекламная компания не удалась. За 30 минут не набралось 10 человек, Ваш баланс сохранился."
                )

                model_task.active = False
                model_user = await model_task.user.get()
                model_task.coins_after_ending = model_user.balance
                await model_task.save()

                for task_s in model_task_storage:
                    user = await task_s.user.get()
                    await main_bot.send_message(
                        chat_id=user.id,
                        text=f"К сожалению, на задание с моделью {user.model_nickname} не набралось достаточно людей. Можете закрыть ссылку с ней."
                    )

                    task_s.failed = True
                    task_s.finished = True
                    await task_s.save()
                continue

            if model_task.started:
                if model_task.end_time < time.time():
                    model_user = await model_task.user.get()
                    await main_bot.send_message(
                        chat_id=model_user.id,
                        text=f"Ваша рекламная компания удалась. С Вашего счета списано {model_task.working * cost}"
                    )

                    model_task.active = False
                    model_task.finished = True
                    model_user.balance -= model_task.working * cost

                    await model_task.save()
                    await model_user.save()
