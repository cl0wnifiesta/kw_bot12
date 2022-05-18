from config import dp
from aiogram import executor
from db_manager import DatabaseManager
import middlewares
import handlers


async def on_startup(_):
    await DatabaseManager().create_tables()
    print("Бот онлайн")

if __name__ == "__main__":
    middlewares.setup(dp)
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
