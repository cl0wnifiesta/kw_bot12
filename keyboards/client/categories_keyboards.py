from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from config import base

categories_kb = InlineKeyboardMarkup(row_width=1)

categories_kb.add(InlineKeyboardMarkup(text="🇺🇦Украина", callback_data="category_ukraine"))
categories_kb.add(InlineKeyboardMarkup(text="🇵🇱Польша", callback_data="category_poland"))
categories_kb.add(InlineKeyboardMarkup(text="🇺🇸США", callback_data="category_usa"))

async def get_product_kb(region):
    products = await base.get_product_list(region)
    keyboard = InlineKeyboardMarkup(row_width=1)
    for product in products:
        keyboard.add(InlineKeyboardButton(text=f'{product[0]} | {product[1]}р | {("Остаток: " + str(product[2])) if product[2] !=0 else "[Товар закончился]"}', callback_data=f'product_{product[3]}'))
    keyboard.add(InlineKeyboardButton(text="🔙Назад", callback_data="back_category"))
    return keyboard

