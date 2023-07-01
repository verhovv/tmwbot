import asyncio

from aiogram import Router, Bot, Dispatcher

from handlers.start import router as start_router
from handlers.lang_choose import router as lang_router
from settings import TOKEN

from database import database

router = Router()
router.include_router(start_router)
router.include_router(lang_router)

bot = Bot(TOKEN, parse_mode="HTML")


async def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)

    async with asyncio.TaskGroup() as tg:
        tg.create_task(dp.start_polling(bot))
        tg.create_task(database.init())


if __name__ == "__main__":
    asyncio.run(main())
