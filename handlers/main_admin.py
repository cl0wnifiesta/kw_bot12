from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import dp, bot, admins, base


from handlers.client import start_message

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.admin.admin_kb import main_admin_kb
from keyboards.client.main_keyboard import main_kb


@dp.message_handler(commands="admin", user_id=admins)
async def admin_main(message: types.Message):
    await message.answer("Меню админ-панели", reply_markup=main_admin_kb)

@dp.message_handler(Text(equals="↩Вернуться в режим пользователя"), user_id=admins)
async def get_back_to_user(message: types.Message, state: FSMContext):
    await bot.send_message(message.from_user.id, "Добро пожаловать в магазин 🔥 фарм аккаунтов по приемлемым ценам 💵. "
                                                 "Продажа аккаунтов только в одни руки 🤲.", reply_markup=main_kb)
    await state.finish()

@dp.callback_query_handler(Text("adm_close"))
async def admin_close(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await state.finish()
