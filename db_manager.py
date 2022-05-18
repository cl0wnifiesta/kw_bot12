import aiosqlite

class DatabaseManager:
    async def create_tables(self):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS "users" (
	            "username" TEXT,
	            "userid" INT,
	            "referal_id" INT,
	            "discount" INT,
	            "balance" INT,
	            "purchases" INT,
	            PRIMARY KEY("userid")
            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "promos" (
                "promo_text" TEXT,
                "procent" INT,
                "usage_amount" INT,
                PRIMARY KEY("promo_text")
            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "sub_categories" (
                "id" INT,
                "category" TEXT,
                "name" TEXT,
                "price" INT,
                "count" INT,
                "description" TEXT,
                PRIMARY KEY("name")
            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "product_info" (
                "sub_category" TEXT,
                "fio" TEXT,
                "login" TEXT,
                "password" TEXT,
                "mail" TEXT,
                "mail_pass" TEXT,
                "geo" TEXT,
                "date_of_birth" TEXT,
                "reg_date" TEXT,
                "id" TEXT,
                "friends" TEXT,
                "cookie" TEXT,
                "date_of_extradition" TEXT,
                "eaab" TEXT,
                "fan_page" TEXT,
                "user_agent" TEXT,
                "photo_selfie" TEXT,
                "pk_id" TEXT,
                "bm_id" TEXT,
                "bm_token" TEXT,
                "bm_link" TEXT
             );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "product_info" """)
            await db.commit()



    async def user_exists(self, userid):
        async with aiosqlite.connect('database.db') as db:
            return bool(await (await db.execute("""SELECT username FROM users WHERE userid == ?""", (int(userid),))).fetchall())

    async def add_user(self, username, userid, referal):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO users(userid, username, referal_id, discount, balance, purchases) 
                            VALUES (?, ?, ?, ?, ?, ?)""", (username, userid, referal, 0, 0, 0))
            await db.commit()

    async def get_users_id(self):
        async with aiosqlite.connect('database.db') as db:
            users = await db.execute("""SELECT userid FROM users""")
            return await users.fetchall()

    async def get_all_users_info(self):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT userid, username, balance FROM users""")
            users = await ex.fetchall()
            return users

    async def change_user_balance(self, new_balance, userid):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""UPDATE users SET balance == ? WHERE userid == ?""", (int(new_balance), int(userid)))
            await db.commit()

    async def get_detail_user_info(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM users WHERE userid == ?""", (int(userid),))
            return await ex.fetchone()

    async def get_promos(self):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM promos""")
            return await ex.fetchall()

    async def add_promo(self, promo_text, procent, amount_of_usage):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO promos(promo_text, procent, usage_amount) 
                                VALUES(?, ?, ?)""", (promo_text, int(procent), int(amount_of_usage)))
            await db.commit()

    async def remove_promo(self, promo_text):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""DELETE FROM promos WHERE promo_text == ?""", (promo_text,))
            await db.commit()

    async def get_product_list(self, region):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT name, price, count, id FROM sub_categories WHERE category == ?""", (region,))
            return await ex.fetchall()

    async def get_category_by_product_id(self, product_id):
        async with aiosqlite.connect('database.db') as db:
            return (await (await db.execute("SELECT category FROM sub_categories WHERE id == ?", (product_id,))).fetchone())[0]

    async def add_product(self, region, name, price, description):
        async with aiosqlite.connect('database.db') as db:
            count = 0
            product_id = 1
            products = await (await db.execute("""SELECT id FROM sub_categories""")).fetchall()
            if len(products):
                while (product_id,) in products:
                    product_id += 1
            await db.execute("""INSERT INTO sub_categories(id, category, name, price, count, description)
                            VALUES(?, ?, ?, ?, ?, ?);""", (product_id, region, name, price, count, description))
            await db.commit()

    async def update_product_setting(self, setting, data, product):
        async with aiosqlite.connect('database.db') as db:
            if setting == 'name':
                await db.execute(
                    """UPDATE sub_categories SET name == ? WHERE id == ?""", (data, int(product)))
            elif setting == 'text':
                await db.execute(
                    """UPDATE sub_categories SET description == ? WHERE id == ?""", (data, int(product)))
            elif setting == 'price':
                await db.execute(
                    """UPDATE sub_categories SET price == ? WHERE id == ?""", (int(data), int(product)))
            await db.commit()

    async def delete_product(self, product_id):
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                """DELETE FROM sub_categories WHERE id == ?""", (int(product_id),))
            await db.execute(
                """DELETE FROM product_info WHERE sub_category == ?""", (int(product_id),))
            await db.commit()

    async def delete_product_info(self, product_id):
        async with aiosqlite.connect('database.db') as db:
            await db.execute(
                """DELETE FROM product_info WHERE sub_category == ?""", (int(product_id),))
            await db.execute("""UPDATE sub_categories SET count == ? WHERE id == ?""", (0, int(product_id)))
            await db.commit()

    async def input_product_info(self, product_info_list):
        async with aiosqlite.connect('database.db') as db:
            await db.executemany("""INSERT INTO product_info(sub_category, fio, login, password, mail, mail_pass, geo,
                                                            date_of_birth, reg_date, id, friends, cookie, date_of_extradition,
                                                            eaab, fan_page, user_agent, photo_selfie, pk_id, bm_id, bm_token, bm_link)
                                                VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""", product_info_list)
            category_id = product_info_list[0][0]
            count_of_product = (await (await db.execute("""SELECT count FROM sub_categories WHERE id == ?""", (category_id, ))).fetchone())[0]
            await db.execute("""UPDATE sub_categories SET count == ? WHERE id == ?""", (int(count_of_product) + len(product_info_list), category_id))
            await db.commit()

    async def get_count_of_product(self, product_id):
        async with aiosqlite.connect('database.db') as db:
            return (await (await db.execute("""SELECT count FROM sub_categories WHERE id == ?""", (product_id, ))).fetchone())[0]

    async def get_product_info(self, product_id):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM sub_categories WHERE id == ?""", (int(product_id),))
            return await ex.fetchone()

    async def get_sell_info(self, product_id, count):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT fio, login, password, mail, mail_pass, geo,
                                            date_of_birth, reg_date, id, friends, cookie, date_of_extradition,
                                            eaab, fan_page, user_agent, photo_selfie, pk_id, bm_id, bm_token, bm_link FROM product_info WHERE sub_category == ?""", (str(product_id), ))
            return await ex.fetchmany(int(count))
