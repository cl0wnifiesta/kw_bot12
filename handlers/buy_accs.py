import random
from aiofiles import os

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types

from config import dp, bot, base, qiwi_p2p, log_chat_id

from states.client_states import BuyProduct
from keyboards.client.categories_keyboards import categories_kb, get_product_kb
from keyboards.admin.admin_kb import cancel_kb
from keyboards.client.payment_keyboards import get_payment_kb
from utils.get_product import get_product_sell_info


@dp.message_handler(Text(equals="💼Купить аккаунты"))
async def get_categories_list(message: types.Message):
    await bot.send_message(message.from_user.id, "Активные категории в магазине:", reply_markup=categories_kb)


@dp.callback_query_handler(Text(startswith="category_"))
async def get_product_list(call: types.CallbackQuery):
    region = call.data.split("_")[1]
    await call.message.edit_text("Активные подкатегории:", reply_markup=await get_product_kb(region))


@dp.callback_query_handler(Text(startswith="product_"))
async def buy_product_show_menu(callback: types.CallbackQuery, state: FSMContext):
    product_number = callback.data.split("_")[1]
    product_info = await base.get_product_info(product_number)
    await callback.message.delete()
    await BuyProduct.get_count.set()
    async with state.proxy() as data:
        data['message_id'] = (await callback.message.answer(f"<b>🈳Товар:</b> {product_info[2]}\n"
                                                            f"<b>💸Цена за 1 штуку товара:</b> {product_info[3]}\n"
                                                            f"<b>📙В наличии:</b> {product_info[4]}\n\n"
                                                            f"<b>📃Описание:</b>\n {product_info[5]}\n\n"
                                                            f"<em>Введите количество товара, которое вы хотите приобрести:</em>",
                                                            reply_markup=cancel_kb)).message_id
        data['product'] = product_number

    await callback.answer()

@dp.message_handler(state=BuyProduct.get_count)
async def get_count_of_product(message: types.Message, state: FSMContext):
    try:
        async with state.proxy() as data:
            data['count'] = int(message.text)
            sub_category_count = await base.get_count_of_product(data['product'])
            if not (0 < data['count'] <= sub_category_count):
                await bot.edit_message_text("<b>❌Такого количества товара нет в наличии</b>\n\n"
                                            "<em>❗Доступное количество товара указано в информации о самом товаре!</em>",
                                            message.from_user.id, data['message_id'])
                await message.delete()
                await state.finish()
                return
            await message.answer('Выберите способ оплаты:',
                                 reply_markup=await get_payment_kb(data['product'], data['count']))
        await state.finish()
    except ValueError:
        async with state.proxy() as data:
            await bot.edit_message_text("<b>❌Неверный ввод, попробуйте снова</b>",
                                        message.from_user.id, data['message_id'])
            await message.delete()
            await state.finish()


@dp.callback_query_handler(Text(startswith="buy_qiwi_"))
async def buy_product_operation(callback: types.CallbackQuery, state: FSMContext):
    try:
        await qiwi_p2p.reject(bill_id=new_bill.bill_id)
    except:
        pass
    count = callback.data.split("_")[3]
    product = callback.data.split("_")[2]
    random_chars_part = list("1234567890abcdefGHIGKLMNOPQRSTUVYXWZ")
    random.shuffle(random_chars_part)
    password_chars_part = "".join(
        [random.choice(random_chars_part) for x in range(10)])
    password_number_part = str(random.randint(100000000000, 999999999999))
    bill_id_result = password_number_part + password_chars_part
    product_info = await base.get_product_info(product)
    user_info = await base.get_detail_user_info(callback.from_user.id)
    userid = callback.from_user.id
    if await base.is_user_have_promo(userid):
        user_promo_text = await base.get_user_promo(userid)
        promo = await base.get_promo_info(user_promo_text)
        if promo[3] <= int(count) * int(product_info[3]):
            amount = (int(count) * int(product_info[3])) - int(((int(count) * int(product_info[3])) / 100) * user_info[4])
        else:
            amount = (int(count) * int(product_info[3]))
    else:
        amount = (int(count) * int(product_info[3]))
    new_bill = await qiwi_p2p.bill(bill_id=bill_id_result, amount=amount, lifetime=12)
    await callback.message.edit_text("➖➖➖➖Чек оплаты➖➖➖➖\n"
                                     f"<b>Чтобы начать оплату нажмите на кнопку ниже и вас переадресует на страницу оплаты.\n</b>"
                                     f"<b>Счёт будет действителен <code>12 минут</code>. После оплаты нажмите на кнопку ПРОВЕРИТЬ ОПЛАТУ </b>\n\n"
                                     f"💰Сумма оплаты: <code>{new_bill.amount}</code>\n"
                                     f"📝Номер заказа: <code>{bill_id_result}</code>\n\n"
                                     f"<em>❗Не изменяйте данных по ссылке оплаты! В противном случае ваш платёж может не засчитаться</em>",
                                     reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                         InlineKeyboardButton(text="Перейти к оплате", url=new_bill.pay_url)).add(
                                         InlineKeyboardButton(text="🔎Проверить оплату",
                                                              callback_data=f"check_bill_{bill_id_result}_{product}_{count}_{amount}")).add(
                                         InlineKeyboardButton(text="❌Отменить оплату",
                                                              callback_data=f"reject_bill_{bill_id_result}")))
    await callback.answer()


@dp.callback_query_handler(Text(startswith="check_bill_"))
async def check_qiwi_payment(callback: types.CallbackQuery):
    p2p_check = await qiwi_p2p.check(callback.data.split("_")[2])
    amount = callback.data.split("_")[5]
    count = callback.data.split("_")[4]
    product = callback.data.split("_")[3]
    userid = callback.from_user.id
    username = callback.from_user.username
    if p2p_check.status == 'PAID':
        try:
            await callback.message.delete()
            bill_id = callback.data.split("_")[2]
            if int(await base.get_referal(callback.from_user.id)) != 0:
                await base.referal_add(int(await base.get_referal(callback.from_user.id)), int((int(amount) / 100) * 10))
            await base.user_sell_mixin(userid)
            await callback.message.answer(f"<b>✅Оплата счёта <code>{bill_id}</code> прошла успешно</b>")
            sell_files = await get_product_sell_info(product, count, bill_id)
            await base.add_sell_to_logs(bill_id, userid, amount)
            await callback.message.answer_document(open(sell_files['excel'], 'rb'))
            await callback.message.answer_document(open(sell_files['txt'], 'rb'))
            await bot.send_message(log_chat_id, 'Новая покупка!\n'
                                                f'Айди пользователя: {callback.from_user.id}\n'
                                                f'Номер заказа: {callback.data.split("_")[2]}\n'
                                                f'Сумма заказа: {amount}\n')
            await bot.send_document(log_chat_id, open(sell_files['excel'], 'rb'))
            await os.remove(sell_files['excel'])
            await os.remove(sell_files['txt'])
        except Exception as e:
            print(e)
            await callback.message.edit_text("Ошибка")
    elif p2p_check.status == 'WAITING':
        await callback.message.answer("❌Счёт ещё не оплачен")
    elif p2p_check.status == 'REJECTED':
        await callback.message.answer("❌Счёт отклонён")
    elif p2p_check.status == 'EXPIRED':
        await callback.message.answer("❌Время жизни счёта истекло. Попробуйте снова")
    await callback.answer()


@dp.callback_query_handler(Text(startswith="reject_bill_"))
async def buy_product_reject_qiwi_payment(callback: types.CallbackQuery):
    try:
        await qiwi_p2p.reject(callback.data.split("_")[2])
        await callback.message.answer("<b>❌Счёт на оплату отменён</b>")
    except:
        await callback.message.answer("<b>❌Счёта не существует</b>")
    await callback.message.delete()
    await callback.answer()

@dp.callback_query_handler(Text(startswith="buy_balance_"))
async def buy_product_by_balance(call: types.CallbackQuery):
    product = call.data.split("_")[2]
    count = call.data.split("_")[3]
    userid = call.from_user.id
    random_chars_part = list("1234567890abcdefGHIGKLMNOPQRSTUVYXWZ")
    random.shuffle(random_chars_part)
    password_chars_part = "".join(
        [random.choice(random_chars_part) for x in range(10)])
    password_number_part = str(random.randint(100000000000, 999999999999))
    bill_id_result = password_number_part + password_chars_part
    product_info = await base.get_product_info(product)
    user_info = await base.get_detail_user_info(call.from_user.id)
    if await base.is_user_have_promo(userid):
        user_promo_text = await base.get_user_promo(userid)
        promo = await base.get_promo_info(user_promo_text)
        if promo[3] <= int(count) * int(product_info[3]):
            amount = (int(count) * int(product_info[3])) - int(((int(count) * int(product_info[3])) / 100) * user_info[4])
        else:
            amount = (int(count) * int(product_info[3]))
    else:
        amount = (int(count) * int(product_info[3]))
    balance = await base.get_user_balance(call.from_user.id)
    if balance < amount:
        await call.message.edit_text("⭕Ошибка! \n\nНа вашем балансе недостаточно средст для покупки")
        return
    try:
        await call.message.delete()
        bill_id = bill_id_result
        if int(await base.get_referal(call.from_user.id)) != 0:
            await base.referal_add(int(await base.get_referal(call.from_user.id)), int((int(amount) / 100) * 10))
        await base.user_sell_mixin(userid)
        await call.message.answer(f"<b>✅Оплата счёта <code>{bill_id}</code> прошла успешно</b>")
        sell_files = await get_product_sell_info(product, count, bill_id)
        await base.add_sell_to_logs(bill_id, userid, amount)
        await base.change_user_balance(balance - amount, call.from_user.id)
        await call.message.answer_document(open(sell_files['excel'], 'rb'))
        await call.message.answer_document(open(sell_files['txt'], 'rb'))
        await bot.send_message(log_chat_id, 'Новая покупка!\n'
                                            f'Айди пользователя: {call.from_user.id}\n'
                                            f'Номер заказа: {bill_id_result}\n'
                                            f'Сумма заказа: {amount}\n')
        await bot.send_document(log_chat_id, open(sell_files['excel'], 'rb'))
        await os.remove(sell_files['excel'])
        await os.remove(sell_files['txt'])
    except Exception as e:
        print(e)
        await call.message.edit_text("Ошибка")


@dp.callback_query_handler(Text('back_category'))
async def get_back_to_categories(call: types.CallbackQuery):
    await call.message.edit_text("Активные категории в магазине:", reply_markup=categories_kb)
