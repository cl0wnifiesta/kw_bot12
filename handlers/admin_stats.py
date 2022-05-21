from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, admins, base

from aiogram.dispatcher.filters import Text

from keyboards.admin.admin_kb import admin_stats_kb


@dp.message_handler(Text("📊Статистика"), user_id=admins)
async def get_admin_stats(message: types.Message):
    stats = await base.get_admin_stats()
    await message.answer("➖➖➖➖<b>📊Статистика</b>➖➖➖➖\n"
                         f"👥Всего пользователей бота: <code>{stats[0]}</code>\n"
                         f"🛒Всего продано товаров: <code>{stats[1]}</code>\n"
                         f'👑Пользователь который купил наибольшее количество товара: <a href="tg://user?id={str(stats[2])}">@{await base.get_username_by_id(stats[2])}</a>\n'
                         f"💵Общая сумма покупок: <code>{str(stats[3])} рублей</code>", reply_markup=admin_stats_kb)


@dp.callback_query_handler(Text("get_admin_stats"), user_id=admins)
async def get_admin_stats(call: types.CallbackQuery):
    stats = await base.get_admin_stats()
    await call.message.edit_text("➖➖➖➖<b>📊Статистика</b>➖➖➖➖\n"
                                 f"👥Всего пользователей бота: <code>{stats[0]}</code>\n"
                                 f"🛒Всего продано товаров: <code>{stats[1]}</code>\n"
                                 f'👑Пользователь который купил наибольшее количество товара: <a href="tg://user?id={str(stats[2])}">@{await base.get_username_by_id(stats[2])}</a>\n'
                                 f"💵Общая сумма покупок: <code>{str(stats[3])} рублей</code>",
                                 reply_markup=admin_stats_kb)


@dp.callback_query_handler(Text("admin_stats_day"))
async def get_day_stats(call: types.CallbackQuery):
    stats = await base.get_day_admin_stats()
    msg = ("➖➖➖➖💰Покупки за день➖➖➖➖\n\n"
           "<strong>ID | Сумма | Номер заказа</strong>\n\n")
    for buy in stats:
        msg += f"{buy[0]} | {buy[1]} | {buy[2]}\n"
    await call.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="Назад", callback_data="get_admin_stats")))


@dp.callback_query_handler(Text("admin_stats_week"))
async def get_day_stats(call: types.CallbackQuery):
    stats = await base.get_week_admin_stats()
    msg = ("➖➖➖➖💰Покупки за неделю➖➖➖➖\n\n"
           "<strong>ID | Сумма | Номер заказа</strong>\n\n")
    for buy in stats:
        msg += f"{buy[0]} | {buy[1]} | {buy[2]}\n"
    await call.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="Назад", callback_data="get_admin_stats")))


@dp.callback_query_handler(Text("admin_stats_month"))
async def get_day_stats(call: types.CallbackQuery):
    stats = await base.get_month_admin_stats()
    msg = ("➖➖➖➖💰Покупки за месяц➖➖➖➖\n\n"
           "<strong>ID | Сумма | Номер заказа</strong>\n\n")
    for buy in stats:
        msg += f"{buy[0]} | {buy[1]} | {buy[2]}\n"
    await call.message.edit_text(msg, reply_markup=InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton(text="Назад", callback_data="get_admin_stats")))

