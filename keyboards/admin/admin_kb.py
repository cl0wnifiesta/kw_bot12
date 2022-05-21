from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup

main_admin_kb = ReplyKeyboardMarkup(resize_keyboard=True)

main_admin_kb.row("💬Изменение сообщений", "💼Товары")
main_admin_kb.row("📢Рассылка", "👨Пользователи")
main_admin_kb.row("📊Статистика", "📄Промокоды")
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

change_command_kb = InlineKeyboardMarkup(row_width=1)
change_command_kb.add(InlineKeyboardButton(text="Правила", callback_data="command_change_rules"))
change_command_kb.add(InlineKeyboardButton(text="Поддержка", callback_data="command_change_help"))
change_command_kb.add(InlineKeyboardButton(text="Акции", callback_data="command_change_stock"))
change_command_kb.add(InlineKeyboardButton(text="Альтернативные способы оплаты", callback_data="command_change_altpayment"))
change_command_kb.add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close"))

admin_stats_kb = InlineKeyboardMarkup(row_width=2)
admin_stats_kb.add(InlineKeyboardButton(text="За день", callback_data="admin_stats_day"))
admin_stats_kb.add(InlineKeyboardButton(text="За неделю", callback_data="admin_stats_week"))
admin_stats_kb.add(InlineKeyboardButton(text="За месяц", callback_data="admin_stats_month"))
admin_stats_kb.add(InlineKeyboardButton(text="Закрыть", callback_data="adm_close"))

