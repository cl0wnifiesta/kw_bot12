from aiogram.utils.executor import start_webhook

from config import dp, bot
from aiogram import executor
from db_manager import DatabaseManager
import middlewares
import handlers

WEBHOOK_HOST = 'https://e7f1-109-234-34-41.eu.ngrok.io' # сюда ссылку из Ngrok
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

# webserver settings
WEBAPP_HOST = 'localhost'  # or ip
WEBAPP_PORT = 80


async def on_startup(_):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(_):

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == 'main':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )

