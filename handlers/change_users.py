from aiogram import types
from config import dp, bot, admins, base

from keyboards.admin.admin_kb import detail_user_kb, get_change_balance_kb
from states.admin_states import UserDetailView, ChangeUserBalance

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text


@dp.message_handler(Text(equals="👨Пользователи"), state=None, user_id=admins)
async def get_all_users_stats(message: types.Message):
    answer_text = "<strong>ID | Usename </strong>\n"
    for user in await base.get_all_users_info():
        answer_text += f'{user[0]} | <a href="tg://user?id={str(user[0])}">{user[1]}</a>\n'
    await message.answer(answer_text, reply_markup=detail_user_kb)

@dp.callback_query_handler(Text(equals="detail_user"), state=None)
async def detail_user_view(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("Введите айди пользователя:")
    await UserDetailView.get_user_id.set()
    async with state.proxy() as data:
        data['message_id'] = call.message.message_id
    await call.answer()

@dp.message_handler(state=UserDetailView.get_user_id)
async def get_user_id_for_detail_view(message: types.Message, state: FSMContext):
    try:
        if await base.user_exists(int(message.text)):
            user_stats = await base.get_detail_user_info(message.text)
            await message.answer("➖➖➖➖<b>👤Профиль пользователя</b>➖➖➖➖\n"
                                 f'🈹Пользователь: <a href="tg://user?id={str(user_stats[1])}">@{user_stats[0]}</a>\n'
                                 f"🆔ID пользователя: <code>{str(user_stats[1])}</code>\n"
                                 f"👨‍Реферал: <code>{str(user_stats[2]) if user_stats[2]!=0 else 'Нет'}</code>\n"
                                 f"💸Баланс: <code>{str(user_stats[4])}</code> рублей\n"
                                 f"🛒Количество покупок: <code>{str(user_stats[5])}</code>\n",
                                 reply_markup=get_change_balance_kb(user_stats[1]))
    except ValueError:
        await message.answer("Неверный ввод!")
    finally:
        await state.finish()

@dp.callback_query_handler(Text(startswith="change_balance_"), state=None)
async def change_user_balance(call: types.CallbackQuery, state: FSMContext):
    await ChangeUserBalance.get_balance.set()
    async with state.proxy() as data:
        data['message_id'] = (await call.message.answer("Введите новое число баланса пользователя:")).message_id
        data['user_id'] = call.data.split("_")[2]
    await call.answer()

@dp.message_handler(state=ChangeUserBalance.get_balance)
async def change_user_balance(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            await base.change_user_balance(message.text, data['user_id'])
            await bot.delete_message(message.from_user.id, message.message_id)
            await bot.edit_message_text(f'✅Баланс <a href="tg://user?id={str(data["user_id"])}">пользователя</a> '
                                        f'теперь {message.text}', chat_id=message.from_user.id,
                                        message_id=data['message_id'])
    except ValueError:
        await message.answer("Неверный ввод!")
    finally:
        await state.finish()

