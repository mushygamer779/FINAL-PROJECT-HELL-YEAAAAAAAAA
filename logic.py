import sqlite3

class BotFunc:
    def __init__(self, db_name):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tegUsers (
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
        
    def register_user(self, user_id, username, age, degree_yn, speciality, have_device_laptop, state):
        self.cursor.execute('''INSERT INTO tegUsers 
                            (user_id, username, age, degree_yn, speciality, have_device_laptop, state)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                            ON CONFLICT(user_id) DO UPDATE SET
                                username = excluded.username,
                                age = excluded.age,
                                degree_yn = excluded.degree_yn,
                                speciality = excluded.speciality,
                                have_device_laptop = excluded.have_device_laptop,
                                state = excluded.state''',
                            (user_id, username, age, degree_yn, speciality, have_device_laptop, state))
        self.conn.commit()
   

    def showAllUsers(self):
        self.cursor.execute('SELECT * FROM tegUsers')
        rows = self.cursor.fetchall()
        columns = ['id', 'user_id', 'username', 'age', 'degree_yn', 'speciality', 'have_device_laptop', 'state']
        return [dict(zip(columns, row)) for row in rows]

    def update_user(self, user_id, username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state=None):
        self.cursor.execute('''SELECT * FROM tegUsers WHERE user_id = ?''', (user_id,))
        user = self.cursor.fetchone()
        if user:
            updated_username = username if username is not None else user[2]
            updated_age = age if age is not None else user[3]
            updated_degree_yn = degree_yn if degree_yn is not None else user[4]
            updated_speciality = speciality if speciality is not None else user[5]
            updated_have_device_laptop = have_device_laptop if have_device_laptop is not None else user[6]
            updated_state = state if state is not None else user[7]

            self.cursor.execute('''UPDATE tegUsers SET 
                                   username = ?, 
                                   age = ?, 
                                   degree_yn = ?, 
                                   speciality = ?, 
                                   have_device_laptop = ?, 
                                   state = ? 
                                   WHERE user_id = ?''',
                                (updated_username, updated_age, updated_degree_yn, updated_speciality, updated_have_device_laptop, updated_state, user_id))
            self.conn.commit()
        # self.conn.close()


    def delete_user(self, user_id):
        self.cursor.execute('''DELETE FROM tegUsers WHERE user_id = ?''', (user_id,))
        self.conn.commit()
   


if __name__ == "__main__":
    bot_func = BotFunc("tegUsers.db")
    bot_func.create_table()
    print("This is the logic module.")
    # bot_func.delete_user('6666483906')