from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext

from states.admin_states import CreatePromo, PromoRemove
from config import dp, bot, admins, base
from keyboards.admin.admin_kb import cancel_kb, choose_promo

@dp.message_handler(Text(equals="📄Промокоды"), user_id=admins, state=None)
async def promo_choose(message: types.Message, state: FSMContext):
    answer_text = "<strong>Текст</strong> | <strong>Процент скидки</strong> | <strong>Кол-во использований</strong> | <strong>Интервал</strong>:\n\n"
    for promo in await base.get_promos():
        answer_text += f"{promo[0]} | {promo[1]}% | Остаток: {promo[2]} | Интервал: от {promo[3]}\n\n"
    await message.answer(answer_text, reply_markup=choose_promo)

@dp.callback_query_handler(Text("promo_remove"))
async def remove_promo(call: types.CallbackQuery, state: FSMContext):
    await PromoRemove.get_name.set()
    async with state.proxy() as data:
        data['message_id'] = (
            await call.message.edit_text("Введите текст промокода:", reply_markup=cancel_kb)).message_id

@dp.message_handler(state=PromoRemove.get_name)
async def get_promo_text(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            await base.remove_promo(message.text)
            await bot.edit_message_text("❗Промокод успешно удалён", chat_id=message.from_user.id,
                                        message_id=data['message_id'])
        except:
            await bot.edit_message_text("❎Ошибка: такого промокода не существует", chat_id=message.from_user.id,
                                        message_id=data['message_id'],
                                        )
        finally:
            await message.delete()
            await state.finish()

@dp.callback_query_handler(Text("promo_add"))
async def create_promo(call: types.CallbackQuery, state: FSMContext):
    await CreatePromo.get_promo_text.set()
    async with state.proxy() as data:
        data['message_id'] = (await call.message.edit_text("Введите текст промокода:", reply_markup=cancel_kb)).message_id

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
            await bot.edit_message_text("Введите интервал промокода (c какой суммы начинает действовать):",
                                        chat_id=message.from_user.id, message_id=data['message_id'],
                                        reply_markup=cancel_kb)
    except ValueError:
        await message.answer("❌Неправильный ввод!")
        await state.finish()

@dp.message_handler(state=CreatePromo.get_interval)
async def get_promo_text(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['interval'] = int(message.text)
            await message.delete()
            await base.add_promo(data['text'], data['procent'], data['amount_of_usage'], data['interval'])
            await bot.edit_message_text("✅Промокод успешно добавлен!\n\n"
                                        f"Текст: <strong>{data['text']}</strong>\n"
                                        f"Скидка: <code>{str(data['procent'])}%</code>\n"
                                        f"Количество использований: <code>{str(data['amount_of_usage'])}</code>\n"
                                        f"Интервал промокода: от <code>{str(data['interval'])}</code> руб",
                                        chat_id=message.from_user.id, message_id=data['message_id'])
    except ValueError:
        await message.answer("❌Неправильный ввод!")
    finally:
        await state.finish()

@dp.callback_query_handler(Text(equals="adm_cancel"), state="*")
async def adm_cancel(call: types.CallbackQuery, state: FSMContext):
    await call.message.delete()
    await bot.send_message(call.from_user.id, "Действие отменено")
    await state.finish()
