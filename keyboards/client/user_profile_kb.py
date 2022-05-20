from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


async def get_profile_kb(userid):
    profile_kb = InlineKeyboardMarkup(row_width=1)
    profile_kb.add(InlineKeyboardButton(text="Реферальная система", callback_data=f"profile_ref_{userid}"))
    profile_kb.add(InlineKeyboardButton(text="Правила", callback_data=f"get_rules_{userid}"))
    profile_kb.add(InlineKeyboardButton(text="Альтернативные способы оплаты", callback_data=f"profile_altpayment_{userid}"))
    profile_kb.add(InlineKeyboardButton(text="История заказов", callback_data=f"profile_history_{userid}"))
    profile_kb.add(InlineKeyboardButton(text="Активировать промокод", callback_data=f"profile_promo_activate_{userid}"))
    profile_kb.add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close"))
    return profile_kb

async def get_profile_button(userid):
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"get_profile_{userid}"))
    return keyboard

async def get_referal_keyboard(userid):
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(InlineKeyboardButton(text="Рефералы", callback_data=f"get_referals_{userid}"))
    keyboard.add(InlineKeyboardButton(text="Назад", callback_data=f"get_profile_{userid}"))
    return keyboard
