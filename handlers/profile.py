from aiogram import Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import base, dp, bot

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from states.client_states import InputPromo
from keyboards.client.user_profile_kb import get_profile_kb, get_profile_button, get_referal_keyboard
from keyboards.admin.admin_kb import cancel_kb

@dp.message_handler(Text("👨‍💼Профиль"))
async def user_profile(message: types.Message = None):
    user_stats = await base.get_detail_user_info(message.from_user.id)
    await message.answer("➖➖➖<b>👤Профиль пользователя</b>➖➖➖\n"
                         f'🈹Пользователь: <a href="tg://user?id={str(user_stats[1])}">@{user_stats[0]}</a>\n'
                         f"🆔ID пользователя: <code>{str(user_stats[1])}</code>\n"
                         f"👨Айди реферала: <code>{str(user_stats[2]) if user_stats[2] != 0 else 'Нет'}</code>\n"
                         f"💸Сумма начислений с реферальной системы: <code>{user_stats[3]}</code> рублей\n"
                         f"💸Баланс: <code>{str(user_stats[5])}</code> рублей\n" 
                         f"💯Скидка: <code>{str(user_stats[4])}</code> %\n"
                         f"🛒Количество покупок: <code>{str(user_stats[6])}</code>\n", reply_markup=await get_profile_kb(message.from_user.id))

@dp.callback_query_handler(Text(startswith="get_profile_"))
async def user_profile(call: types.CallbackQuery):
    user_stats = await base.get_detail_user_info(call.from_user.id)
    await call.message.edit_text("➖➖➖<b>👤Профиль пользователя</b>➖➖➖\n"
                                 f'🈹Пользователь: <a href="tg://user?id={str(user_stats[1])}">@{user_stats[0]}</a>\n'
                                 f"🆔ID пользователя: <code>{str(user_stats[1])}</code>\n"
                                 f"👨Айди реферала: <code>{str(user_stats[2]) if user_stats[2] != 0 else 'Нет'}</code>\n"
                                 f"💸Сумма начислений с реферальной системы: <code>{user_stats[3]}</code> рублей\n"
                                 f"💸Баланс: <code>{str(user_stats[5])}</code> рублей\n"
                                 f"💯Скидка: <code>{str(user_stats[4])}</code> %\n"
                                 f"🛒Количество покупок: <code>{str(user_stats[6])}</code>\n", reply_markup=await get_profile_kb(call.from_user.id))

@dp.callback_query_handler(Text(startswith="get_rules_"))
async def get_rules(call: types.CallbackQuery):
    await call.message.edit_text(await base.get_command_text('rules'),
                                 reply_markup=await get_profile_button(call.from_user.id))

@dp.callback_query_handler(Text(startswith="profile_altpayment_"))
async def get_rules(call: types.CallbackQuery):
    await call.message.edit_text(await base.get_command_text('altpayment'),
                                 reply_markup=await get_profile_button(call.from_user.id))

@dp.callback_query_handler(Text(startswith="profile_ref_"))
async def get_user_ref(call: types.CallbackQuery):
    await call.message.edit_text(f"Реферальная система в нашем боте!\n\n"
                                 f"<strong>Приглашайте друзей и получайте деньги на баланс</strong>!\n\n"
                                 f"Вы будете получать <strong>10%</strong> от каждой покупки пригласившего\n\n"
                                 f"<strong>Ваша реферальная ссылка</strong>: https://t.me/FBshop2020_bot?start={call.from_user.id}",
                                 reply_markup=await get_referal_keyboard(call.from_user.id))

@dp.callback_query_handler(Text(startswith="profile_promo_activate_"))
async def activate_promo(call: types.CallbackQuery, state: FSMContext):
    await InputPromo.get_text.set()
    await call.message.edit_text("📄Введите промокод:", reply_markup=cancel_kb)
    async with state.proxy() as data:
        data['message_id'] = call.message.message_id

@dp.message_handler(state=InputPromo.get_text)
async def get_promo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            promo_info = await base.get_promo_info(message.text)
            if promo_info[2] != 0:
                if await base.is_promo_used(message.from_user.id, message.text):
                    await bot.edit_message_text("Ошибка ввода промокода: вы уже вводили этот промокод!",
                                                chat_id=message.from_user.id, message_id=data['message_id'])
                    await state.finish()
                    return
                if await base.is_user_have_promo(message.from_user.id):
                    await bot.edit_message_text(
                        "Ошибка ввода промокода: у вас уже есть активированный промокод!",
                        chat_id=message.from_user.id, message_id=data['message_id'])
                    await state.finish()
                    return
                await base.activate_promo(message.from_user.id, promo_info[0], promo_info[1])
                await bot.edit_message_text("💯Промокод активирован!", chat_id=message.from_user.id, message_id=data['message_id'])
            else:
                await bot.edit_message_text(
                    "Ошибка ввода промокода: превышено максимальное количество использования промокодов!",
                    chat_id=message.from_user.id, message_id=data['message_id'])
        except:
            await bot.edit_message_text("Ошибка ввода промокода: промокод не найден",
                                        chat_id=message.from_user.id, message_id=data['message_id'])
        finally:
            await state.finish()

@dp.callback_query_handler(Text(startswith="get_referals_"))
async def get_referals(call: types.CallbackQuery):
    userid = call.data.split("_")[2]
    referals = await base.get_referals_stats(userid)
    msg = "📦Список приглашённых пользователей:\n\n"
    for referal in referals:
        msg += f'<a href="tg://user?id={str(referal[0])}">@{referal[1]}</a>\n'
    await call.message.edit_text(msg,
                                 reply_markup=InlineKeyboardMarkup(row_width=1)
                                 .add(InlineKeyboardButton(text="Назад",
                                                           callback_data=f"profile_ref_{userid}")))

@dp.callback_query_handler(Text(startswith="profile_history_"))
async def get_user_history(call: types.CallbackQuery):
    userid = call.data.split("_")[2]
    orders = await base.get_user_order_history(userid)
    msg = "<strong>💰История ваших покупок</strong>:\n\n" \
          "Номер заказа | Цена\n\n"
    for order in orders:
        msg += f'{order[2]} | {order[1]} рублей\n '
    await call.message.edit_text(msg,
                                 reply_markup=InlineKeyboardMarkup(row_width=1)
                                 .add(InlineKeyboardButton(text="Назад",
                                                           callback_data=f"get_profile_{userid}")))
