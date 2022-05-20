from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, admins, base


from handlers.client import start_message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.admin.admin_kb import main_admin_kb


@dp.message_handler(commands="admin", user_id=admins)
async def admin_main(message: types.Message):
    await message.answer("Меню админ-панели", reply_markup=main_admin_kb)

@dp.message_handler(Text(equals="↩Вернуться в режим пользователя"), state=None, user_id=admins)
async def get_back_to_user(message: types.Message):
    await start_message(message)

@dp.callback_query_handler(Text("adm_close"))
async def admin_close(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()

@dp.message_handler(Text("📊Статистика"), user_id=admins)
async def get_admin_stats(message: types.Message):
    stats = await base.get_admin_stats()
    await message.answer("➖➖➖➖<b>📊Статистика</b>➖➖➖➖\n"
                           f"👥Всего пользователей бота: <code>{stats[0]}</code>\n"
                           f"🛒Всего продано товаров: <code>{stats[1]}</code>\n"
                           f'👑Пользователь который купил наибольшее количество товара: <a href="tg://user?id={str(stats[2])}">@{await base.get_username_by_id(stats[2])}</a>\n'
                           f"💵Общая сумма покупок: <code>{str(stats[3])} рублей</code>", reply_markup=InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close")))