from aiogram import types

from config import base, bot, admins


async def get_stats(message: types.Message, user_id=admins):
    stats = await base.get_all_stats()
    await bot.send_message(message.from_user.id, "➖➖➖➖<b>📊Статистика</b>➖➖➖➖\n"
                           f"👥Всего пользователей бота: <code>{stats[0]}</code>\n"
                           f"🛒Всего продано товаров: <code>{stats[1]}</code>\n"
                           f'👑Пользователь который купил наибольшее количество товара: <a href="tg://user?id={str(stats[3])}">@{base.get_username_by_id(message.from_user.id)}</a>\n'
                           f"💵Общая сумма покупок: <code>{str(stats[4])} рублей</code>")