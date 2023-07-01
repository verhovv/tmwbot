from tortoise import Tortoise, run_async


async def init() -> None:
    await Tortoise.init(
        db_url='sqlite://database/db.sqlite3',
        modules={'models': ['bot.database.models']}
    )

    await Tortoise.generate_schemas()
