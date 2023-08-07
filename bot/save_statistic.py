import time
from collections import defaultdict
from datetime import datetime

import pandas
from aiogram import Bot

from bot.config import time_modes
from bot.database.models import Tasks


async def save_statistic(bot: Bot):
    data = defaultdict(list)

    tasks = await Tasks.filter(finished=True)

    for task in tasks:
        user = await task.user.get()
        username = (await bot.get_chat_member(chat_id=user.id, user_id=user.id)).user.username
        datetime_obj = datetime.fromtimestamp(task.start_time)
        data['Номер задания'].append(task.id)
        data['Дата, время'].append(
            f'{datetime_obj.day}.{datetime_obj.month}.{datetime_obj.year} | {datetime_obj.hour}:{datetime_obj.minute}')
        data['Имя модели'].append(user.model_nickname)
        data['Ник тг'].append(('@' + username) if username else 'Скрыто')
        data['Количество выполняющих'].append(task.working)
        data['Время выполнения'].append(time_modes[task.time_mode][0])
        data['Остаток на балансе после выполнения'].append(task.coins_after_ending)

    pandas.DataFrame(data).to_excel('статистика.xlsx', index=False)
