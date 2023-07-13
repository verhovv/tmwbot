from aiogram import Bot
import os

from dotenv import load_dotenv

load_dotenv('.env')

token = os.getenv('TOKEN')
bot = Bot(token, parse_mode="HTML")

BASE_URL = os.getenv('BASE_URL')
channel_id = os.getenv('CHANNEL_ID')
admin_id = os.getenv('ADMIN_ID')