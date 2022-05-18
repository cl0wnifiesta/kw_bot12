from aiogram.utils.executor import start_webhook

from config import dp, bot, admins
from aiogram import executor
from db_manager import DatabaseManager
import handlers, middlewares, keyboards, states, utils

WEBHOOK_HOST = 'https://48f6-109-234-34-41.eu.ngrok.io'
WEBHOOK_PATH = ''
WEBHOOK_URL = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"

WEBAPP_HOST = 'localhost'
WEBAPP_PORT = 5987

async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)
    print(123)
    await bot.send_message(int(admins[0]), "123")


async def on_shutdown(dp):
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )