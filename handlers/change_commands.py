from aiogram import types
from config import dp, bot, admins, base

from keyboards.admin.admin_kb import change_command_kb, cancel_kb
from states.admin_states import ChangeCommand

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

@dp.message_handler(Text("💬Изменение сообщений"), user_id=admins)
async def change_command(message: types.Message, state: FSMContext):
    await message.answer("Выберите команду которую надо изменить:", reply_markup=change_command_kb)

@dp.callback_query_handler(Text(startswith="command_change_"))
async def change_choosen_command(call: types.CallbackQuery, state: FSMContext):
    await ChangeCommand.get_text.set()
    await call.message.edit_text("Введите текст изменённой команды:", reply_markup=cancel_kb)
    async with state.proxy() as data:
        data['command'] = call.data.split("_")[2]
        data['message_id'] = call.message.message_id

@dp.message_handler(state=ChangeCommand.get_text)
async def get_command_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await base.change_command_text(data['command'], message.text)
            await bot.edit_message_text("✅Команда успешно обновлена!", message_id=data['message_id'],
                                        chat_id=message.from_user.id)
        except:
            await bot.edit_message_text("Что-то пошло не так!", message_id=data['message_id'], chat_id=message.from_user.id)
        finally:
            await state.finish()
