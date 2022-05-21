import aiosqlite

class DatabaseManager:
    async def create_tables(self):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""CREATE TABLE IF NOT EXISTS "users" (
	            "username" TEXT,
	            "userid" INT,
	            "referal_id" INT,
	            "referal_sum" INT,
	            "discount" INT,
	            "balance" INT,
	            "purchases" INT,
	            "activated_promo" TEXT,
	            PRIMARY KEY("userid")
            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "promos" (
                "promo_text" TEXT,
                "procent" INT,
                "usage_amount" INT,
                "interval" INT,
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
            await db.execute("""CREATE TABLE IF NOT EXISTS "commands" (
                            "callback" TEXT UNIQUE,
                            "command_text" TEXT,
                            PRIMARY KEY("callback")
                            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "product_logs" (
                            "userid" INT,
                            "sum" INT,
                            "order_id" TEXT,
                            "buy_date" TEXT
                            );""")
            await db.execute("""CREATE TABLE IF NOT EXISTS "promo_logs" (
                             "userid" INT,
                             "promo_text" TEXT
                             );""")
            try:
                commands = [('rules', ''), ('stock', ''), ('altpayment', ''), ('help', ''), ]
                await db.executemany("""INSERT INTO commands(callback, command_text) VALUES(?, ?);""", commands)
            except Exception as e:
                pass
            await db.commit()

    async def user_exists(self, userid):
        async with aiosqlite.connect('database.db') as db:
            return bool(await (await db.execute("""SELECT username FROM users WHERE userid == ?""", (int(userid),))).fetchall())

    async def add_user(self, username, userid, referal):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO users(userid, username, referal_id, discount, balance, purchases, referal_sum) 
                            VALUES (?, ?, ?, ?, ?, ?, ?)""", (username, userid, referal, 0, 0, 0, 0))
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

    async def add_promo(self, promo_text, procent, amount_of_usage, interval):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO promos(promo_text, procent, usage_amount, interval) 
                                VALUES(?, ?, ?, ?)""", (promo_text, int(procent), int(amount_of_usage), int(interval)))
            await db.commit()

    async def is_promo_used(self, userid, promo_text):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM promo_logs WHERE userid == ? AND promo_text == ?""", (userid, promo_text))
            return bool(len(await ex.fetchall()))

    async def is_user_have_promo(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT discount FROM users WHERE userid == ?""", (userid, ))
            if (await ex.fetchone())[0] != 0:
                return True
            return False

    async def get_user_promo(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT activated_promo FROM users WHERE userid == ?""", (userid,))
            return (await ex.fetchone())[0]

    async def get_promo_info(self, promo_text):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM promos WHERE promo_text == ?""", (promo_text, ))
            return await ex.fetchone()

    async def activate_promo(self, userid, promo_text, procent):
        async with aiosqlite.connect('database.db') as db:
            usage_amount = (await (await db.execute("""SELECT usage_amount FROM promos WHERE promo_text == ?""", (promo_text,))).fetchone())[0]
            new_usage_amount = usage_amount - 1
            await db.execute("""UPDATE users SET activated_promo == ? WHERE userid == ?""", (promo_text, userid))
            await db.execute("""UPDATE users SET discount == ? WHERE userid == ?""", (procent, userid))
            await db.execute("""UPDATE promos SET usage_amount == ? WHERE promo_text == ?""", (new_usage_amount, promo_text))
            await db.execute("""INSERT INTO promo_logs(userid, promo_text) VALUES(?, ?);""", (userid, promo_text))
            await db.commit()

    async def remove_promo(self, promo_text):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""DELETE FROM promos WHERE promo_text == ?""", (promo_text,))
            await db.execute("""UPDATE users SET discount == ? WHERE activated_promo == ?""", (0, promo_text))
            await db.execute("""UPDATE users SET activated_promo == ? WHERE activated_promo == ?""", (None, promo_text))
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
            sell_info = await ex.fetchmany(int(count))
            if len(sell_info) < int(count):
                raise Exception
            await db.executemany(("""DELETE FROM product_info WHERE 
                                    fio == ? and login == ? and password == ? and mail == ? and mail_pass == ? and geo == ? and
                                    date_of_birth == ? and reg_date == ? and id == ? and friends == ? and cookie == ? and date_of_extradition == ? and
                                    eaab == ? and fan_page == ? and user_agent == ? and photo_selfie == ? and pk_id == ? and bm_id == ? and bm_token == ? and
                                    bm_link == ?"""), sell_info)
            current_count = await db.execute("""SELECT count FROM sub_categories WHERE id == ?""", (product_id,))
            current_count = (await current_count.fetchone())[0]
            new_count = current_count - int(count)
            await db.execute("""UPDATE sub_categories SET count == ? WHERE id == ?""", (new_count, product_id))
            await db.commit()
            return sell_info

    async def user_sell_mixin(self, userid):
        async with aiosqlite.connect('database.db') as db:
            purchases = (await (await db.execute("""SELECT purchases FROM users WHERE userid == ?""", (userid,))).fetchone())[0]
            new_purchases = purchases + 1
            await db.execute("""UPDATE users SET purchases == ? WHERE userid == ?""", (new_purchases, userid))
            await db.commit()

    async def change_command_text(self, command_callback, command_text):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""UPDATE commands SET command_text == ? WHERE callback == ?""", (command_text, command_callback))
            await db.commit()

    async def get_command_text(self, command_callback):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT command_text FROM commands WHERE callback == ?""", (command_callback,))
            return (await ex.fetchone())[0]

    async def get_referals_stats(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT userid, username FROM users WHERE referal_id == ?""", (userid,))
            return await ex.fetchall()

    async def get_referal(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT referal_id FROM users WHERE userid == ?""", (int(userid),))
            return (await ex.fetchone())[0]

    async def referal_add(self, userid, summ):
        async with aiosqlite.connect('database.db') as db:
            current_ref_summ = (await (await db.execute("""SELECT referal_sum FROM users WHERE userid == ?""", (userid, ))).fetchone())[0]
            balance = (await (await db.execute("""SELECT balance FROM users WHERE userid == ?""", (userid, ))).fetchone())[0]
            new_balance = balance + summ
            await db.execute("""UPDATE users SET referal_sum == ? WHERE userid == ?""", (int(current_ref_summ)+summ, userid))
            await db.execute("""UPDATE users SET balance == ? WHERE userid == ?""", (new_balance, userid))
            await db.commit()

    async def add_sell_to_logs(self, bill_id, userid, amount):
        async with aiosqlite.connect('database.db') as db:
            await db.execute("""INSERT INTO product_logs(userid, sum, order_id, buy_date) VALUES(?, ?, ?, datetime('now'));""", (userid, amount, bill_id))

            await db.commit()

    async def get_user_order_history(self, userid):
        async with aiosqlite.connect('database.db') as db:
            ex = await db.execute("""SELECT * FROM product_logs WHERE userid == ?""", (userid,))
            return await ex.fetchall()

    async def get_admin_stats(self):
        async with aiosqlite.connect('database.db') as db:
            logs_count = len(await (await db.execute("""SELECT * FROM product_logs""")).fetchall())
            user_count = len(await (await db.execute("""SELECT * FROM users""")).fetchall())
            if logs_count == 0:
                best_client, price_array = 'Нет', (0,)
            else:
                logs_client_info = await (await db.execute("""SELECT userid FROM product_logs""")).fetchall()
                logs_price_info = await (await db.execute("""SELECT sum FROM product_logs""")).fetchall()
                best_client = max(logs_client_info, key=lambda x: logs_client_info.count(x))[0]
                price_array = []
                list(map(lambda x: price_array.append(x[0]), logs_price_info))
            return [user_count, logs_count, best_client, sum(price_array)]

    async def get_username_by_id(self, userid):
        async with aiosqlite.connect('database.db') as db:
            return (await (await db.execute("""SELECT username FROM users WHERE userid == ?""", (userid,))).fetchone())[0]

    async def get_user_balance(self, userid):
        async with aiosqlite.connect('database.db') as db:
            return (await (await db.execute("""SELECT balance FROM users WHERE userid == ?""", (userid,))).fetchone())[0]

    async def get_day_admin_stats(self):
        async with aiosqlite.connect('database.db') as db:

            return await(await db.execute("""SELECT * FROM product_logs WHERE buy_date BETWEEN DATETIME('now', '-1 day') and DATETIME('now') """)).fetchall()

    async def get_week_admin_stats(self):
        async with aiosqlite.connect('database.db') as db:
            return await(await db.execute("""SELECT * FROM product_logs WHERE buy_date BETWEEN DATETIME('now', '-7 day') and DATETIME('now')""")).fetchall()

    async def get_month_admin_stats(self):
        async with aiosqlite.connect('database.db') as db:
            return await(await db.execute("""SELECT * FROM product_logs WHERE buy_date BETWEEN DATETIME('now', '-1 month') and DATETIME('now')""")).fetchall()
