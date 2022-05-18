from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import base

categories_kb = InlineKeyboardMarkup(row_width=1)

categories_kb.add(InlineKeyboardMarkup(text="🇺🇦Украина", callback_data="edit_category_ukraine"))
categories_kb.add(InlineKeyboardMarkup(text="🇵🇱Польша", callback_data="edit_category_poland"))
categories_kb.add(InlineKeyboardMarkup(text="🇺🇸США", callback_data="edit_category_usa"))
categories_kb.add(InlineKeyboardMarkup(text="Закрыть", callback_data="adm_close"))

async def get_product_kb(region):
    products = await base.get_product_list(region)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        keyboard.add(InlineKeyboardButton(text=f'{product[0]} | {product[1]}р | {("Остаток: " + str(product[2])) if product[2] !=0 else "[Товар закончился]"}', callback_data=f'edit_product_{product[3]}'))
    keyboard.add(InlineKeyboardButton(text="📄Добавить новую подкатегорию", callback_data=f"add_product_{region}"))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="admback_category"))
    return keyboard

async def get_edit_products_kb(product_id):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(
        text="🛒Загрузка товара", callback_data="input_product_"+str(product_id)))
    keyboard.add(InlineKeyboardButton(text="✏Изменить название товара",
                 callback_data="change_product_name_"+str(product_id)))
    keyboard.add(InlineKeyboardButton(text="💵Изменить цену товара",
                 callback_data="change_product_price_"+str(product_id)))
    keyboard.add(InlineKeyboardButton(text="💾Изменить описание товара",
                 callback_data="change_product_text_"+str(product_id)))
    keyboard.add(InlineKeyboardButton(text="❎Удалить загруженный товар",
                                      callback_data="delete_info_product_" + str(product_id)))
    keyboard.add(InlineKeyboardButton(text="❎Удалить продукт",
                 callback_data="delete_product_"+str(product_id)))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f'edit_category_{await base.get_category_by_product_id(int(product_id))}'))
    return keyboard

