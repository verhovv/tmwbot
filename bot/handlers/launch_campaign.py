from aiogram import types, Router
from aiogram.filters import Text

from bot.database.models import Users

router = Router()


@router.message(Text(['Launch an advertising campaign', 'Запустить рекламную компанию']))
async def on_launch_campaign_btn(message: types.Message) -> None:
    user = await Users.filter(id=message.from_user.id).first()
    user.state = ''
