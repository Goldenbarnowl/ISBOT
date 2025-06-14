import asyncio
import logging
import sys

from aiogram.methods import DeleteWebhook

from config import dp, bot
from src.routers.user_router import user_router


async def start():
    dp.include_router(user_router)
    try:
        await bot(DeleteWebhook(drop_pending_updates=True))
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(start())
