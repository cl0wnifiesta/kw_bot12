from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import CallbackQuery

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

main_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)

main_admin_kb.row("📢Рассылка", "👨Пользователи")
main_admin_kb.row("📊Статистика", "📄Создать промокод")
main_admin_kb.add("💼Товары")
main_admin_kb.add("↩Вернуться в режим пользователя")

detail_user_kb = InlineKeyboardMarkup(row_width=1)
detail_user_kb.add(InlineKeyboardButton(text="Подробная статистика о пользователе", callback_data="detail_user"))

choose_admin_kb = InlineKeyboardMarkup(row_width=2)
choose_admin_kb.add(InlineKeyboardButton(text="✔️Да", callback_data="choose_yes")).insert(
    InlineKeyboardButton(text="❌Нет", callback_data="choose_no"))

def get_change_balance_kb(userid):
    change_balance_kb = InlineKeyboardMarkup(row_width=1)
    change_balance_kb.add(InlineKeyboardButton(text="Изменить баланс", callback_data=f"change_balance_{str(userid)}"))
    return change_balance_kb

cancel_kb = InlineKeyboardMarkup(row_width=1)
cancel_kb.add(InlineKeyboardButton(text="Отмена", callback_data="adm_cancel"))


choose_promo = InlineKeyboardMarkup(row_width=1)
choose_promo.add(InlineKeyboardButton(text="Создать промокод", callback_data="promo_add"))
choose_promo.add(InlineKeyboardButton(text="Удалить промокод", callback_data="promo_remove"))
choose_promo.add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close"))
