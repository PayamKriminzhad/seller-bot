import sqlite3


class Database:
    def __init__(self, db_file):
        self.db_file = db_file
        self.connection = None

    def connect(self):
        self.connection = sqlite3.connect(self.db_file)

    def disconnect(self):
        self.connection.close()

    def create_tables(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()

            query = '''
                        CREATE TABLE IF NOT EXISTS User (
                            user_id INTEGER PRIMARY KEY,
                            first_name TEXT,
                            user_name TEXT,
                            wallet INTEGER,
                            joined TEXT
                        )
                        '''
            cursor.execute(query)

            query = '''
                        CREATE TABLE IF NOT EXISTS Price (
                            price_id INTEGER PRIMARY KEY,
                            price INTEGER,
                            duration INTEGER,
                            volume TEXT,
                            user TEXT,
                            plan TEXT
                        )
                        '''
            cursor.execute(query)

            query = '''
                        CREATE TABLE IF NOT EXISTS Product (
                            product_id INTEGER PRIMARY KEY,
                            name TEXT,
                            price INTEGER,
                            config TEXT,
                            duration INTEGER,
                            status TEXT,
                            volume TEXT
                        )
                        '''
            cursor.execute(query)

            query = '''
                        CREATE TABLE IF NOT EXISTS Test (
                            test_id INTEGER PRIMARY KEY,
                            user_id TEXT
                        )
                        '''
            cursor.execute(query)

            query = '''
                        CREATE TABLE IF NOT EXISTS Message (
                            message_id INTEGER,
                            user_id TEXT,
                            time INTEGER
                        )
                        '''
            cursor.execute(query)

            query = '''
                                CREATE TABLE IF NOT EXISTS Purchase (
                                    purchase_id TEXT PRIMARY KEY,
                                    user_id INTEGER,
                                    product_id INTEGER,
                                    status TEXT,
                                    date TEXT,
                                    duration INTEGER,
                                    price INTEGER,
                                    volume TEXT,
                                    user TEXT,
                                    expire TEXT,
                                    FOREIGN KEY (user_id) REFERENCES User (user_id),
                                    FOREIGN KEY (product_id) REFERENCES Product (product_id)
                                )
                                '''
            cursor.execute(query)

    def delete_row(self, table_name, condition):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = f'DELETE FROM {table_name} WHERE {condition}'
            cursor.execute(query)

    def get_tables(self):
        with self.connection:
            cursor = self.connection.cursor()
            query = "SELECT name FROM sqlite_master WHERE type='table';"
            cursor.execute(query)
            tables = cursor.fetchall()
            table_names = [table[0] for table in tables]
            return table_names

    def get_product_price(self, product_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = "SELECT price FROM Product WHERE product_id = ?"
            cursor.execute(query, (product_id,))
            result = cursor.fetchone()
            if result is None:
                return None
            return result[0]

    def get_last_purchase_product_id(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            SELECT product_id FROM Purchase 
            WHERE user_id = ? 
            AND status = 'pending'
            ORDER BY purchase_id DESC 
            LIMIT 1
            '''
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def get_last_purchase_id(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            SELECT purchase_id FROM Purchase 
            WHERE user_id = ? 
            AND status = 'pending'
            ORDER BY purchase_id DESC 
            LIMIT 1
            '''
            cursor.execute(query, (user_id,))
            result = cursor.fetchone()
            return result[0] if result else None

    def insert_test(self, test_id, user_id):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                query = '''
                INSERT INTO Test (test_id, user_id) VALUES (?, ?)
                '''
                cursor.execute(query, (test_id, user_id))

    def insert_message(self, message_id, user_id, time):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                query = '''
                INSERT INTO Message (message_id, user_id, time) VALUES (?, ?, ?)
                '''
                cursor.execute(query, (message_id, user_id, time))

    def remove_message(self, message_id, user_id):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                query = '''
                DELETE FROM Message Where message_id = ? AND user_id = ?
                '''
                cursor.execute(query, (message_id, user_id))

    def get_messages(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Message"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            return records

    def get_test_by_user(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Test WHERE user_id = ?"""
            cursor.execute(sqlite_select_query, (user_id,))
            records = cursor.fetchall()
            return records

    def insert_product(self, product_id, name, price, config, duration, status, volume):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            INSERT INTO Product (product_id, name, price, config, duration, status, volume) VALUES (?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (product_id, name, price, config, duration, status, volume))

    def insert_user(self, user_id, first_name, user_name, wallet, joined):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            INSERT INTO User (user_id, first_name, user_name, wallet, joined) VALUES (?, ?, ?, ?, ?)
                '''
            cursor.execute(query, (user_id, first_name, user_name, wallet, joined))

    def update_user_wallet(self, amount, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = "UPDATE User SET wallet = ? WHERE user_id = ?"
            cursor.execute(query, (amount, user_id))

    def get_users(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM User"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            return records

    def get_user_by_id(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM User WHERE user_id = ?"""
            cursor.execute(sqlite_select_query, (user_id,))
            records = cursor.fetchall()
            return records

    def get_purchase_by_id(self, purchase_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Purchase WHERE purchase_id = ?"""
            cursor.execute(sqlite_select_query, (purchase_id,))
            records = cursor.fetchall()
            return records
    
    def get_confirmed_purchase_by_user(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Purchase WHERE user_id = ? AND status='confirmed' ORDER BY purchase_id DESC"""
            cursor.execute(sqlite_select_query, (user_id,))
            records = cursor.fetchall()
            return records

    def insert_purchase(self, purchase_id, user_id, product_id, status, date, duration, price, volume, user, expire):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            INSERT INTO Purchase (purchase_id, user_id, product_id, status, date, duration, price, volume, user, expire) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (purchase_id, user_id, product_id, status, date, duration, price, volume, user, expire))

    def update_purchase_status(self, purchase_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """UPDATE Purchase SET status = 'confirmed' WHERE purchase_id = ? AND status='pending'"""
            cursor.execute(query, (purchase_id,))

    def update_purchase_status_to_expired(self, purchase_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = """UPDATE Purchase SET status = 'expired' WHERE purchase_id = ? AND status='confirmed'"""
            cursor.execute(query, (purchase_id,))

    def get_product_by_name(self, name):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Product WHERE name= ? AND status='available'"""
            cursor.execute(sqlite_select_query, (name,))
            records = cursor.fetchall()
            return records

    def get_available_products(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Product WHERE status='available';"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            return records
            
    def get_unavailable_products(self):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                sqlite_select_query = """SELECT * FROM Product WHERE status='unavailable';"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                return records

    def get_confirmed_purchases(self):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                sqlite_select_query = """SELECT * FROM Purchase WHERE status='confirmed' OR status='expired';"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                return records

    def get_pending_purchases(self):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                sqlite_select_query = """SELECT * FROM Purchase WHERE status='pending';"""
                cursor.execute(sqlite_select_query)
                records = cursor.fetchall()
                return records

    def update_product_status(self, product_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = "UPDATE Product SET status = 'unavailable' WHERE product_id = ?"
            cursor.execute(query, (product_id,))

    def delete_product(self, config):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = "DELETE FROM Product WHERE config = ?"
            cursor.execute(query, (config,))

    def get_user_purchase(self, user_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Purchase WHERE user_id= ? ORDER BY purchase_id DESC LIMIT 1"""
            cursor.execute(sqlite_select_query, (user_id,))
            records = cursor.fetchall()
            return records

    def get_price(self, duration, volume, user, plan):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Price WHERE duration = ? AND volume = ? AND user = ? AND plan=?"""
            cursor.execute(sqlite_select_query, (duration, volume, user, plan))
            records = cursor.fetchall()
            return records
    
    def get_all_prices(self):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Price"""
            cursor.execute(sqlite_select_query)
            records = cursor.fetchall()
            return records

    def insert_price(self, price_id, price, duration, volume, user, plan):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            query = '''
            INSERT INTO Price (price_id, price, duration, volume, user, plan) VALUES (?, ?, ?, ?, ?, ?)
            '''
            cursor.execute(query, (price_id, price, duration, volume, user, plan))

    def update_price(self, price, duration, volume, user, plan):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                query = """UPDATE Price SET price = ? WHERE duration = ? AND volume =? AND user=? AND plan=?"""
                cursor.execute(query, (price, duration, volume, user, plan))
    
    def update_purchase_date(self, date, expire, purchase_id):
            with sqlite3.connect(self.db_file) as conn:
                cursor = conn.cursor()
                query = """UPDATE Purchase SET date = ?, expire = ? WHERE purchase_id = ?"""
                cursor.execute(query, (date, expire, purchase_id,))

    def get_product_by_id(self, product_id):
        with sqlite3.connect(self.db_file) as conn:
            cursor = conn.cursor()
            sqlite_select_query = """SELECT * FROM Product WHERE product_id= ?"""
            cursor.execute(sqlite_select_query, (product_id,))
            records = cursor.fetchall()
            return records