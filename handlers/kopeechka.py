from aiofiles import os
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram import types
from bs4 import BeautifulSoup

import requests

from config import dp, bot, kopeechka_token
from keyboards.admin.admin_kb import cancel_kb
from keyboards.client.main_keyboard import main_kb
from keyboards.client.kopeechka_kb import kopeechka_choose1, kopeechka_choose2
from states.client_states import GetEmailCode


@dp.message_handler(Text("🤖Получить код с почты"))
async def email_code_get_email(message: types.Message, state: FSMContext):
    await GetEmailCode.get_email.set()
    await message.answer("Введите email аккаунта:", reply_markup=cancel_kb)


@dp.message_handler(state=GetEmailCode.get_email)
async def email_code_get_types(message: types.Message, state: FSMContext):
    await GetEmailCode.next()
    await message.answer("Какое сообщение вы хотите получить?", reply_markup=kopeechka_choose1)
    async with state.proxy() as data:
        data['email'] = message.text


@dp.message_handler(state=GetEmailCode.get_type)
async def email_code_request_email(message: types.Message, state: FSMContext):
    await GetEmailCode.next()
    if message.text == "Только код":
        async with state.proxy() as data:
            data['type'] = 'only_code'
        await message.answer("Нажмите в фейсбуке получить код на почту, после этого нажмите 'Код отправлен'", reply_markup=kopeechka_choose2)
    elif message.text == "Полное письмо":
        async with state.proxy() as data:
            data['type'] = 'full_msg'
        await message.answer("Нажмите в фейсбуке получить код на почту, после этого нажмите 'Код отправлен'", reply_markup=kopeechka_choose2)
    elif message.text == "⬅Отмена":
        await message.answer("Действие отменено", reply_markup=main_kb)
        await state.finish()


@dp.message_handler(state=GetEmailCode.code_sended)
async def email_code_request_email(message: types.Message, state: FSMContext):
    if message.text == "Код отправлен":
        async with state.proxy() as data:
            mail = data['email']
            msg_type = data['type']
        site = 'Facebook.com'
        subject = 'confirmation code'
        response1 = requests.get(
            f'http://api.kopeechka.store/mailbox-reorder?site={site}&email={mail}&token={kopeechka_token}&api=2.0')
        if response1.json()['status'] == 'ERROR':
            if response1.json()['value'] == 'NO_ACTIVATION':
                await message.answer('Почта не найдена', reply_markup=main_kb)
                await state.finish()
            if response1.json()['value'] == 'SYSTEM_ERROR':
                await message.answer('Неизвестная ошибка! Обратитесь в тех. поддержку', reply_markup=main_kb)
                await state.finish()
        else:
            await message.answer("✅Запрос отправлен!\n\nЧтобы проверить готовность письма нажмите кнопку ниже",
                                 reply_markup=InlineKeyboardMarkup(row_width=1).add(
                                     InlineKeyboardButton(text="Проверить готовность",
                                                          callback_data=f"email_code_check_{response1.json()['id']}_{msg_type}")))
            await state.finish()
    elif message.text == "⬅Отмена":
        await message.answer('Действие отменено', reply_markup=main_kb)
        await state.finish()

@dp.callback_query_handler(Text(startswith="email_code_check_"))
async def email_check_code(call: types.CallbackQuery):
    email_id = call.data.split("_")[3]
    msg_type = call.data.split("_")[4]
    response2 = requests.get(
        f'https://api.kopeechka.store/mailbox-get-message?full=1&spa=1&id={email_id}&token={kopeechka_token}')
    if response2.json()['status'] == 'ERROR':
        if response2.json()['value'] == 'NO_ACTIVATION':
            await call.message.answer("Айди активации не найдено", reply_markup=main_kb)
            await call.message.delete()
        elif response2.json()['value'] == 'ACTIVATION_CANCELED':
            await call.message.answer("Почта была отменена", reply_markup=main_kb)
            await call.message.delete()
        elif response2.json()['value'] == 'WAIT_LINK':
            await call.message.answer("Письмо ещё не получено!", reply_markup=main_kb)

    elif response2.json()['status'] == 'OK':
        if msg_type == 'only_code':
            soup = BeautifulSoup(response2.json()['fullmessage'], 'html.parser')
            temp1 = soup.find('td',
                              style='font-size:11px;font-family:LucidaGrande,tahoma,verdana,arial,sans-serif;padding:10px;background-color:#f2f2f2;border-left:none;border-right:none;border-top:none;border-bottom:none;')
            code = temp1.find('span').get_text()
            await call.message.answer(f"Код получен!\n\n<strong>{code}</strong>")
            await call.message.delete()
        elif msg_type == 'full_msg':
            with open(f'products/{email_id}.html', "w") as f:
                f.write(response2.json()['fullmessage'])
            await bot.send_document(call.from_user.id, open(f'products/{email_id}.html', 'rb'), caption="Письмо получено!\n\nВнутри HTML файла находится код страницы письма", reply_markup=main_kb)
            await os.remove(f'products/{email_id}.html')
            await call.message.delete()
        await call.answer()
