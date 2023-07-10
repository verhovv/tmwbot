import asyncio

from aiogram import Router, Dispatcher

from handlers.start import router as start_router
from handlers.lang_choose import router as lang_router
from handlers.launch_campaign import router as launch_campaign_router
from handlers.run_campaign import router as run_campaign_router
from handlers.buy_points import router as buy_points_router
from handlers.sell_points import router as sell_points_router
from config import bot as main_bot

from filters import ChannelFilter

from database import database

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


if __name__ == "__main__":
    asyncio.run(main())
