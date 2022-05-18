import aiogram
from aiogram.utils.executor import start_webhook

from config import dp, bot
from aiogram import executor
from db_manager import DatabaseManager
import middlewares
import handlers


WEBHOOK_HOST = '109.234.34.41'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % '5365166446:AAEe740Q5yPT2IlHdsFvKACr9xSH6ASN8xk'


async def on_startup(_):
    await DatabaseManager().create_tables()
    await bot.set_webhook(url=WEBHOOK_URL_BASE, certificate=open(WEBHOOK_SSL_CERT, 'r'))
    print("Бот онлайн")

async def on_shutdown(_):
    await bot.delete_webhook()

if __name__ == "__main__":
    middlewares.setup(dp)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_URL_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host='localhost',
        port=3001)
