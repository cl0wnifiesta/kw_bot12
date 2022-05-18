from aiogram.dispatcher.filters.state import State, StatesGroup

class BuyProduct(StatesGroup):
    get_count = State()
    get_payment_method = State()
