import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import router
from config import config

from db.base import create_tables

storage = MemoryStorage()


bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(storage=storage)


async def main():
    dp.include_router(router)
    await create_tables()
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот выключен!')
