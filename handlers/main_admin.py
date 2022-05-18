from aiogram import Dispatcher, types
from config import dp, bot, admins


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
