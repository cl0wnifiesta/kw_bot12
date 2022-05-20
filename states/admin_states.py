from aiogram.dispatcher.filters.state import State, StatesGroup

class DoMailingList(StatesGroup):
    get_text = State()
    get_choose = State()

class UserDetailView(StatesGroup):
    get_user_id = State()

class ChangeUserBalance(StatesGroup):
    get_balance = State()

class CreatePromo(StatesGroup):
    get_promo_text = State()
    get_procent = State()
    get_amount_of_usage = State()
    get_interval = State()

class GetProducts(StatesGroup):
    get_product_file = State()

class AddSubcategory(StatesGroup):
    get_name = State()
    get_price = State()
    get_description = State()

class UpdateProduct(StatesGroup):
    get_data = State()

class PromoRemove(StatesGroup):
    get_name = State()

class ChangeCommand(StatesGroup):
    get_text = State()
