from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import ContentType

import os
import pandas as pd
import openpyxl

from states.admin_states import GetProducts, AddSubcategory, UpdateProduct
from config import dp, bot, admins, base
from keyboards.admin.admin_kb import cancel_kb
from keyboards.admin.admin_product_kbs import categories_kb, get_product_kb, get_edit_products_kb
from utils.df_convert import convert_dict_of_df_to_list


@dp.message_handler(Text("💼Товары"), state=None, user_id=admins)
async def edit_categories(message: types.Message, state: FSMContext):
    await message.answer("⚙Выберите категорию:", reply_markup=categories_kb)

@dp.callback_query_handler(Text(startswith="edit_category_"))
async def show_categories_to_edit(call: types.CallbackQuery):
    region = call.data.split("_")[2]
    await call.message.edit_text("📋Выберите товар:", reply_markup=await get_product_kb(region))

@dp.callback_query_handler(Text(startswith="add_product_"), state=None)
async def add_new_subcategory(call: types.CallbackQuery, state: FSMContext):
    region = call.data.split("_")[2]
    await call.message.edit_text("📃Введите название:", reply_markup=cancel_kb)
    await AddSubcategory.get_name.set()
    async with state.proxy() as data:
        data['category'] = region
        data['message_id'] = call.message.message_id

@dp.message_handler(state=AddSubcategory.get_name)
async def add_new_subcategory(message: types.message, state: FSMContext):
    await AddSubcategory.next()
    async with state.proxy() as data:
        data['name'] = message.text
        await bot.edit_message_text("💵Введите цену:", message_id=data['message_id'], chat_id=message.from_user.id, reply_markup=cancel_kb)
    await bot.delete_message(message.from_user.id, message.message_id)

@dp.message_handler(state=AddSubcategory.get_price)
async def add_new_subcategory(message: types.message, state: FSMContext):
    await AddSubcategory.next()
    async with state.proxy() as data:
        try:
            data['price'] = int(message.text)
            await bot.edit_message_text("💾Введите описание подкатегории:", message_id=data['message_id'],
                                        chat_id=message.from_user.id, reply_markup=cancel_kb)
        except ValueError:
            await bot.edit_message_text("Неверный ввод!", message_id=data['message_id'],
                                        chat_id=message.from_user.id)
            await state.finish()
        finally:
            await bot.delete_message(message.from_user.id, message.message_id)

@dp.message_handler(state=AddSubcategory.get_description)
async def add_new_subcategory(message: types.message, state: FSMContext):
    async with state.proxy() as data:
        try:
            data['description'] = message.text
            await base.add_product(data['category'], data['name'], data['price'], data['description'])
            await bot.edit_message_text("<strong>✅Подкатегория успешно добавлена!</strong>", message_id=data['message_id'],
                                        chat_id=message.from_user.id)
        except ValueError:
            await bot.edit_message_text("Неверный ввод!", message_id=data['message_id'],
                                        chat_id=message.from_user.id)
        finally:
            await state.finish()
            await bot.delete_message(message.from_user.id, message.message_id)

@dp.callback_query_handler(Text(startswith="edit_product_"), state=None)
async def edit_product(call: types.CallbackQuery):
    product_id = call.data.split("_")[2]
    await call.message.edit_text("📎Выберите действие:", reply_markup=await get_edit_products_kb(int(product_id)))

@dp.callback_query_handler(Text(startswith="change_product_"))
async def change_product(call: types.CallbackQuery, state: FSMContext):
    await UpdateProduct.get_data.set()
    async with state.proxy() as data:
        data['setting'] = call.data.split("_")[2]
        data['product'] = call.data.split("_")[3]
        data['message_id'] = call.message.message_id
    await call.message.edit_text("<b>📄Введите новое значение:</b>", reply_markup=cancel_kb)
    await call.answer()

@dp.message_handler(state=UpdateProduct.get_data)
async def get_change_product_data(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['data'] = message.text
        try:
            await base.update_product_setting(data['setting'], data['data'], data['product'])
        except:
            await bot.edit_message_text("<b>❌Неверный ввод, попробуйте снова.</b>\n\n"
                                        "<em>❗На ввод цены принимаются только числа!</em>", chat_id=message.from_user.id, message_id=int(data['message_id']))
            await bot.delete_message(message.from_user.id, message.message_id)
            await state.finish()
            return
        await bot.delete_message(message.from_user.id, message.message_id)
        await bot.edit_message_text("<b>✅Обновлено\n\n</b>"
                                    "<b>📎Выберите действие:</b>", message.from_user.id, int(data['message_id']), reply_markup=await get_edit_products_kb(data['product']))
        await state.finish()

@dp.callback_query_handler(Text(startswith="delete_product_"))
async def edit_products_delete_product(callback: types.CallbackQuery, state: FSMContext):
    product_id = callback.data.split("_")[2]
    region = await base.get_category_by_product_id(int(product_id))
    await base.delete_product(product_id)
    await callback.message.edit_text("<b>✅Подкатегория успешно удалёна</b>\n\n"
                                     "<b>⚙ Выберите товар который требуется настроить:</b>", reply_markup=await get_product_kb(region))
    await callback.answer()

@dp.callback_query_handler(Text(startswith="input_product_"))
async def input_products(call: types.CallbackQuery, state: FSMContext):
    await GetProducts.get_product_file.set()
    product_id = call.data.split("_")[2]
    category = await base.get_category_by_product_id(product_id)
    async with state.proxy() as data:
        data['message_id'] = (await call.message.answer("💾Загрузите файл (в формате xlsx) с товаром:", reply_markup=cancel_kb)).message_id
        data['product_id'] = product_id
        data['chat_id'] = call.from_user.id
        data['category'] = category

@dp.message_handler(state=GetProducts.get_product_file, content_types=types.ContentTypes.DOCUMENT)
async def get_product_file(message: types.Message, state: FSMContext):
    try:
        destination = f'products/{message.document.file_id}.xlsx'
        await bot.download_file_by_id(message.document.file_id, destination)
        wb = openpyxl.load_workbook(destination)
        sheet = wb.get_sheet_names()[0]
        products_df = pd.read_excel(destination, sheet_name=sheet)
        products_dict = products_df.to_dict()
        print(products_dict)
        async with state.proxy() as data:
            data_in_list = convert_dict_of_df_to_list(data['product_id'], products_dict)
            await base.input_product_info(data_in_list)
            await bot.edit_message_text("✅Товар успешно загружен", message_id=data['message_id'], chat_id=data['chat_id'])
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test.txt')
        os.remove(destination)
    except:
        async with state.proxy() as data:
            await bot.edit_message_text("Неверный ввод", message_id=data['message_id'], chat_id=message.from_user.id)
    finally:
        await state.finish()

@dp.callback_query_handler(Text(startswith="delete_info_product_"))
async def delete_product_info(call: types.CallbackQuery):
    product_id = call.data.split("_")[3]
    region = await base.get_category_by_product_id(int(product_id))
    await base.delete_product_info(product_id)
    await call.message.edit_text("<b>✅Загруженные товары подкатегории успешно удалены!</b>\n\n"
                                 "<b>⚙ Выберите действие:</b>",
                                 reply_markup=await get_edit_products_kb(product_id))

@dp.callback_query_handler(Text("admback_category"), state=None)
async def back_to_categories(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text("⚙Выберите категорию:", reply_markup=categories_kb)


