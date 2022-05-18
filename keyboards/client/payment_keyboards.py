from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

async def get_payment_kb(product, count):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Qiwi", callback_data=f"buy_qiwi_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="USDT TRC-20", callback_data=f"buy_usdt_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="С баланса", callback_data=f"buy_balance_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="adm_cancel"))
    return keyboard
