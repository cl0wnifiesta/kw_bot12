import asyncio

import aiofiles
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from pyqiwip2p import AioQiwip2p

from db_manager import DatabaseManager

with open('admins.txt', "r") as file:
    admins = file.read().split("\n")

with open("config.txt", "r") as file:
    file_split = file.read().split()
    qiwi_auth_key = file_split[0].split(":")[1]
    log_chat_id = file_split[1].split(":")[1]

bot = Bot(token='5365166446:AAEe740Q5yPT2IlHdsFvKACr9xSH6ASN8xk', parse_mode="HTML")
storage = MemoryStorage()
base = DatabaseManager()

qiwi_p2p = AioQiwip2p.AioQiwiP2P(auth_key=qiwi_auth_key)

dp = Dispatcher(bot, storage=storage)

