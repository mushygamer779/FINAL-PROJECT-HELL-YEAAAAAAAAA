import sqlite3

class BotFunc:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False) 
        # self.conn = sqlite3.connect(self.db_name) # зачем два раза открывать соединение? можно удалить эту строку и оставить только одну, которая уже открывает соединение с базой данных.
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
                                have_device_laptop TEXT
                            )''')
        self.conn.commit()
        
    def register_user(self, user_id, username, age, degree_yn, speciality, have_device_laptop):
        self.cursor.execute('''INSERT OR IGNORE INTO users 
                               (user_id, username, age, degree_yn, speciality, have_device_laptop)
                               VALUES (?, ?, ?, ?, ?, ?)''',
                            (user_id, username, age, degree_yn, speciality, have_device_laptop))
        self.conn.commit()
        self.conn.close()
    
    def update_user(self, user_id, username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None):
        if username is not None:
            self.cursor.execute('''UPDATE users SET username = ? WHERE user_id = ?''', (username, user_id))
        if age is not None:
            self.cursor.execute('''UPDATE users SET age = ? WHERE user_id = ?''', (age, user_id))
        if degree_yn is not None:
            self.cursor.execute('''UPDATE users SET degree_yn = ? WHERE user_id = ?''', (degree_yn, user_id))
        if speciality is not None:
            self.cursor.execute('''UPDATE users SET speciality = ? WHERE user_id = ?''', (speciality, user_id))
        if have_device_laptop is not None:
            self.cursor.execute('''UPDATE users SET have_device_laptop = ? WHERE user_id = ?''', (have_device_laptop, user_id))
        self.conn.commit()


 # создай добавление пользователя в базу данных при регистрации, чтобы не держать всех пользователей в памяти. при регистрации пользователя, сохраняй его данные в базе данных, а не в списке Users. тогда тебе не нужно будет использовать глобальную переменную Users и работать с ней, а просто сохранять данные в базе данных и при необходимости извлекать их оттуда.
    def add_user(self, user_id, username, age, degree_yn, speciality, have_device_laptop):
        self.cursor.execute('''INSERT INTO users (user_id, username, age, degree_yn, speciality, have_device_laptop) 
                               VALUES (?, ?, ?, ?, ?, ?)''', 
                            (user_id, username, age, degree_yn, speciality, have_device_laptop))
        self.conn.commit()
    # просмотр базы данных
    def get_users(self) -> list:
        self.cursor.execute('''SELECT * FROM users''')
        users = self.cursor.fetchall()
        return users
 # c большой буквы пишутся классы и константы, а не функции. лучше назвать эту функцию delete_user, чтобы было понятно, что это функция для удаления пользователя.
    def delete_user(self, user_id):
        self.cursor.execute('''DELETE FROM users WHERE user_id = ?''', (user_id,))
        self.conn.commit()
        self.conn.close()


if __name__ == "__main__":
    bot_func = BotFunc("users.db")
    # bot_func.create_table() # зачем создавать таблицу при каждом запуске? она же уже создана, если не удалялась. можно удалить эту строку и создать таблицу один раз при инициализации класса, как это сделано в __init__ методе.
    print("This is the logic module.")