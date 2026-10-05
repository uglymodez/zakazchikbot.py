
import asyncio
import os

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from handlers import start, orders      # ← импортируем модули с роутерами

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(
    token=BOT_TOKEN,
    default=DefaultBotProperties(parse_mode="HTML")     # ← вот сюда
)
dp = Dispatcher()


async def main():
    # Подключаем роутеры к диспетчеру
    # Порядок важен: сначала более специфичные, потом общие
    dp.include_router(start.router)
    dp.include_router(orders.router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())