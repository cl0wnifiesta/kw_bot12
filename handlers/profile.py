from aiogram import Dispatcher, types
from kw_bot import dp, config

from keyboards.main_keyboard import main_kb

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton