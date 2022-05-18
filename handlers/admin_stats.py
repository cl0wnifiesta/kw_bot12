from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup

from config import base, dp, bot


async def get_stats(message: types.Message):
    stats = await base.get_all_stats()
    await bot.send_message(message.from_user.id, "➖➖➖➖<b>📊Статистика</b>➖➖➖➖\n"
                           f"👥Всего пользователей бота: <code>{stats[0]}</code>\n"
                           f"🛒Всего продано товаров: <code>{stats[1]}</code>\n"
                           f"🍀Самый продаваемый продукт: <b>{stats[2]}</b>\n"
                           f'👑Пользователь который купил наибольшее количество товара: <a href="tg://user?id={str(stats[3])}">@{base.get_username_by_id(message.from_user.id)}</a>\n'
                           f"💵Общая сумма покупок: <code>{str(stats[4])} рублей</code>")