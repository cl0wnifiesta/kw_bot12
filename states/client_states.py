from aiogram.dispatcher.filters.state import State, StatesGroup

class BuyProduct(StatesGroup):
    get_count = State()
    get_payment_method = State()

class InputPromo(StatesGroup):
    get_text = State()

class GetEmailCode(StatesGroup):
    get_email = State()
    get_type = State()
    code_sended = State()
