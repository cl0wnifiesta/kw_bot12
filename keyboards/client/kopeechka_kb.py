from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup

kopeechka_choose1 = ReplyKeyboardMarkup(resize_keyboard=True)
kopeechka_choose1.add("Только код").add("Полное письмо").add("⬅Отмена")

kopeechka_choose2 = ReplyKeyboardMarkup(resize_keyboard=True)
kopeechka_choose2.add("Код отправлен").add("⬅Отмена")

