from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.admin_states import CreatePromo
from config import dp, bot, admins, base
from keyboards.admin.admin_kb import cancel_kb

@dp.message_handler(Text(equals="📄Создать промокод"), user_id=admins, state=None)
async def create_promo(message: types.Message, state: FSMContext):
    await CreatePromo.get_promo_text.set()
    async with state.proxy() as data:
        data['message_id'] = (await message.answer("Введите текст промокода:", reply_markup=cancel_kb)).message_id

@dp.message_handler(state=CreatePromo.get_promo_text)
async def get_promo_text(message: types.Message, state: FSMContext):
    await CreatePromo.next()
    async with state.proxy() as data:
        data['text'] = message.text
        await message.delete()
        await bot.edit_message_text("Введите процент скидки:", chat_id=message.from_user.id, message_id=data['message_id'],
                                    reply_markup=cancel_kb)

@dp.message_handler(state=CreatePromo.get_procent)
async def get_promo_text(message: types.Message, state: FSMContext):
    await CreatePromo.next()
    try:
        async with state.proxy() as data:
            data['procent'] = int(message.text)
            await message.delete()
            await bot.edit_message_text("Введите кол-во использования промокода:",
                                        chat_id=message.from_user.id, message_id=data['message_id'],
                                        reply_markup=cancel_kb)
    except ValueError:
        await message.answer("❌Неправильный ввод!")
        await state.finish()

@dp.message_handler(state=CreatePromo.get_amount_of_usage)
async def get_promo_text(message: types.Message, state: FSMContext):
    await CreatePromo.next()
    try:
        async with state.proxy() as data:
            data['amount_of_usage'] = int(message.text)
            await message.delete()
            await base.add_promo(data['text'], data['procent'], data['amount_of_usage'])
            await bot.edit_message_text("✅Промокод успешно добавлен!\n\n"
                                        f"Текст: <strong>{data['text']}</strong>\n"
                                        f"Скидка: <code>{str(data['procent'])}%</code>\n"
                                        f"Количество использований: <code>{str(data['amount_of_usage'])}%</code>",
                                        chat_id=message.from_user.id, message_id=data['message_id'])
    except ValueError:
        await message.answer("❌Неправильный ввод!")
        await state.finish()

@dp.callback_query_handler(Text(equals="adm_cancel"), state="*")
async def adm_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "Действие отменено")
    await state.finish()
