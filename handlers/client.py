from aiogram import types
from config import dp, bot, base

from keyboards.client.main_keyboard import main_kb

from aiogram.dispatcher.filters import Text


@dp.message_handler(commands="start")
async def start_message(message: types.Message):
    if not await base.user_exists(message.from_user.id):
        referal = 0
        if " " in message.text:
            try:
                referal = int(message.text.split(" ")[1])
                if referal == message.from_user.id:
                    referal = 0
            except ValueError:
                pass
        await base.add_user(message.from_user.id, message.from_user.username, referal)
    await bot.send_message(message.from_user.id, "Добро пожаловать в магазин 🔥 фарм аккаунтов по приемлемым ценам 💵. "
                                                 "Продажа аккаунтов только в одни руки 🤲.", reply_markup=main_kb)

@dp.message_handler(Text("🆘Поддержка"), state=None)
async def help_message(message: types.Message):
    await message.answer(await base.get_command_text('help'))

@dp.message_handler(Text("🔔Акции"), state=None)
async def help_message(message: types.Message):
    await message.answer(await base.get_command_text('stock'))


