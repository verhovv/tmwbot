import asyncio

from aiogram import Router, Dispatcher

from bot.handlers.start import router as start_router
from bot.handlers.lang_choose import router as lang_router
from bot.handlers.launch_campaign import router as launch_campaign_router
from bot.handlers.run_campaign import router as run_campaign_router
from bot.handlers.buy_points import router as buy_points_router
from bot.handlers.sell_points import router as sell_points_router
from bot.config import bot as main_bot

from bot.filters import ChannelFilter

from bot.database import database

from bot.checker import loop_check

router = Router()
router.message.filter(ChannelFilter())
router.callback_query.filter(ChannelFilter())

router.include_router(start_router)
router.include_router(lang_router)
router.include_router(launch_campaign_router)
router.include_router(run_campaign_router)
router.include_router(buy_points_router)
router.include_router(sell_points_router)


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(dp.start_polling(main_bot))
        tg.create_task(database.init())
        tg.create_task(loop_check())


if __name__ == "__main__":
    asyncio.run(main())
