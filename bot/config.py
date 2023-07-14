from aiogram import Bot
import os

from dotenv import load_dotenv

load_dotenv('.env')

token = os.getenv('TOKEN')
bot = Bot(token, parse_mode="HTML")

BASE_URL = os.getenv('BASE_URL')
channel_id = os.getenv('CHANNEL_ID')
admin_id = os.getenv('ADMIN_ID')

time_modes = {
    'time1': ('55-75 min', 55 * 60, 1),
    'time2': ('115-140 min', 115 * 60, 1.8),
    'time3': ('180-200 min', 180 * 60, 2.4)
}
