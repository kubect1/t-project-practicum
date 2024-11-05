import asyncio

from aiogram import Bot, Dispatcher

from app.core.config import settings
from app.core.db import AsyncSessionLocal
from app.middlewares.db_session_middleware import DBSessionMiddleware
from app.handlers.commands import router as commands_router
from app.handlers.trip_commands import router as trip_commands_router


async def main():
    bot = Bot(token=settings.telegram_bot_token)
    dp = Dispatcher()

    dp.update.middleware(DBSessionMiddleware(session_pool=AsyncSessionLocal))
    dp.include_routers(commands_router, trip_commands_router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
