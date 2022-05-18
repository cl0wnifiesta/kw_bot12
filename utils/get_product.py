from config import base
import pandas
import aiofiles

async def get_product_sell_info(product_id, count, order_num):
    product_info = await base.get_sell_info(product_id, count)
    product_dict = {
        'ФИО': {},
        'Логин': {},
        'Пасс': {},
        'Пароль от почты': {},
        'ГЕО': {},
        'Дата рождения': {},
        'Дата регистрации': {},
        'ID аккаунта': {},
        'Друзья': {},
        'Дата выдачи из базы': {},
        'Токен EAAB': {},
        'Fan Page': {},
        'User Agent': {},
        'Фото для селфи': {},
        'РК ID': {},
        'БМ ID': {},
        'БМ токен': {},
        'БМ ссылка': {}
    }
    for i in range(len(product_info)):
        for header in product_dict:
            product_dict[header][i] = product_info[i][list(product_dict.keys()).index(header)]
    product_df = pandas.DataFrame.from_dict(product_dict)
    excel_destination = f"products/{order_num}.xlsx"
    product_df.to_excel(excel_destination, index=False)
    txt_destination = f"products/{order_num}.txt"
    async with aiofiles.open(txt_destination, "w") as f:
        for i in range(len(product_info)):
            temp = " : ".join(list(product_info[i]))
            await f.write(temp + "\n\n")
    return {"excel": excel_destination, "txt": txt_destination}
