import aiogram

from config import dp, bot
from aiogram import executor
from db_manager import DatabaseManager
import middlewares
import handlers
import cherrypy


WEBHOOK_HOST = '109.234.34.41'
WEBHOOK_PORT = 443  # 443, 80, 88 или 8443 (порт должен быть открыт!)
WEBHOOK_LISTEN = '0.0.0.0'  # На некоторых серверах придется указывать такой же IP, что и выше

WEBHOOK_SSL_CERT = './webhook_cert.pem'  # Путь к сертификату
WEBHOOK_SSL_PRIV = './webhook_pkey.pem'  # Путь к приватному ключу

WEBHOOK_URL_BASE = "https://%s:%s" % (WEBHOOK_HOST, WEBHOOK_PORT)
WEBHOOK_URL_PATH = "/%s/" % '5365166446:AAEe740Q5yPT2IlHdsFvKACr9xSH6ASN8xk'

class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = aiogram.types.Update.as_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            await bot.get_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)

cherrypy.config.update({
    'server.socket_host': WEBHOOK_LISTEN,
    'server.socket_port': WEBHOOK_PORT,
    'server.ssl_module': 'builtin',
    'server.ssl_certificate': WEBHOOK_SSL_CERT,
    'server.ssl_private_key': WEBHOOK_SSL_PRIV
})

async def on_startup(_):
    await DatabaseManager().create_tables()
    # Снимаем вебхук перед повторной установкой (избавляет от некоторых проблем)
    await bot.delete_webhook()

    # Ставим заново вебхук
    bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH,
                    certificate=open(WEBHOOK_SSL_CERT, 'r'))
    print("Бот онлайн")

if __name__ == "__main__":
    middlewares.setup(dp)
    # executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
    cherrypy.quickstart(WebhookServer(), WEBHOOK_URL_PATH, {'/': {}})
