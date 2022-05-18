from aiogram import types
from config import dp, bot, admins

from db_manager import DatabaseManager
from states.admin_states import DoMailingList

from keyboards.admin.admin_kb import choose_admin_kb, cancel_kb

import asyncio

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

base = DatabaseManager()

@dp.message_handler(Text(equals="📢Рассылка"), state=None, user_id=admins)
async def mailing_list(message: types.Message, state: FSMContext):
    edit_message_id = (await bot.send_message(message.from_user.id, "<strong>📨Введите сообщение для рассылки всем пользователем </strong>:\n\n<em>Будьте осторожны, текст нужно вводить строго одним сообщением!</em>", reply_markup=cancel_kb))['message_id']
    await DoMailingList.get_text.set()
    async with state.proxy() as data:
        data['message_id'] = edit_message_id

@dp.message_handler(state=DoMailingList.get_text)
async def mailing_get_text(message: types.Message, state: FSMContext):
    edit_message_id = (await state.get_data()).get('message_id')
    async with state.proxy() as data:
        try:
            data['message'] = message.text
            await bot.edit_message_text(f"<strong>❓Вы уверены в том, что хотите, чтобы это сообщение получило</strong>"
                                        f"<code> {len(await base.get_users_id())} пользователей</code>?", chat_id=message.from_user.id, message_id=edit_message_id, reply_markup=choose_admin_kb)
            await DoMailingList.next()
        except:
            await bot.edit_message_text("❌<strong>Неправильный ввод</strong>\n\n"
                                        "<em>❗На ввод принимается только текст!</em>", chat_id=message.from_user.id, message_id=edit_message_id)
            await state.finish()

@dp.callback_query_handler(Text(startswith="choose_"), state=DoMailingList.get_choose)
async def mailing_process(callback: types.CallbackQuery, state: FSMContext):
    if callback.data.split("_")[1] == "yes":
        await callback.message.edit_text("⏳ <strong>Рассылка началась ...</strong>")
        users = await base.get_users_id()
        message = await state.get_data()
        recieved_users, problem_users = 0, 0
        for user in users:
            try:
                await bot.send_message(user[0], message['message'])
                recieved_users += 1
            except:
                problem_users += 1
            finally:
                await asyncio.sleep(0.3)
        await callback.message.edit_text(f"✉ <b>Рассылка окончена</b>\n\n"
                                         f"<strong>📊 Результат</strong>:\n"
                                         f"Сообщение успешно доставлено <code>{recieved_users}</code> пользователям ✔️\n"
                                         f"Сообщение не было доставлено <code>{problem_users}</code> пользователям ❌")
    else:
        await callback.message.edit_text("✉ <strong>Рассылка успешно отменена ❌</strong>")
    await state.finish()
    await callback.answer()
