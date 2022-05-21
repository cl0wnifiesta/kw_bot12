from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

async def get_payment_kb(product, count):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Qiwi", callback_data=f"buy_qiwi_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="С баланса", callback_data=f"buy_balance_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="Отмена", callback_data="adm_cancel"))
    return keyboard

async def get_buy_by_balance_accept_kb(bill_id, amount, product, count):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="✅Подтвердить покупку",
                                      callback_data=f"balance_buy_accepted_{bill_id}_{amount}_{product}_{count}"))
    keyboard.add(InlineKeyboardButton(text="❎Отменить покупку", callback_data="adm_cancel"))
    return keyboard
