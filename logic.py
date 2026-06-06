import sqlite3

class BotFunc:
    def __init__(self, db_name):
        pass
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER UNIQUE,
                                username TEXT,
                                age INTEGER,
                                degree_yn TEXT,
                                speciality TEXT,
                                have_device_laptop TEXT,
                                state TEXT
                            )''')
        self.conn.commit()
        self.conn.close()

    def register_user(self, user_id, username, age, degree_yn, speciality, have_device_laptop, state):
        self.cursor.execute('''INSERT OR IGNORE INTO users 
                               (user_id, username, age, degree_yn, speciality, have_device_laptop, state)
                               VALUES (?, ?, ?, ?, ?, ?, ?)''',
                            (user_id, username, age, degree_yn, speciality, have_device_laptop, state))
        self.conn.commit()
        self.conn.close()


    def delete_user(self, user_id):
        self.cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    bot_func = BotFunc("users.db")
    bot_func.create_table()
    print("This is the logic module.")
    