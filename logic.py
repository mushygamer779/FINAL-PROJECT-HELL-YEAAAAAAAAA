import sqlite3
import requests
import json
import os
from dotenv import load_dotenv


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
   

    def recommend(self, age: int, has_degree: str, specialty: str, have_device_laptop: str) -> str:
        """
        Generate personalized wealth-building advice using the Google Gemini API.

        Args:
            age                (int): The person's age, e.g. 27
            has_degree         (str): "yes" or "no"
            specialty          (str): Field of study or experience, e.g. "Computer Science"
            have_device_laptop (str): "yes" or "no"

        Returns:
            str: Step-by-step wealth-building roadmap

        Example:
            >>> print(recommend(27, "yes", "Computer Science", "yes"))
        """

        # ── Load env & build URL ──────────────────────────────────────────
        load_dotenv()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={os.getenv('GeminiAPI')}"

        # ── Normalise inputs ──────────────────────────────────────────────
        has_degree         = str(has_degree).strip().lower()
        have_device_laptop = str(have_device_laptop).strip().lower()
        specialty          = str(specialty).strip()

        # ── Build the prompt ──────────────────────────────────────────────
        prompt = f"""You are a world-class financial strategist, entrepreneur, and career coach.

            A person has come to you with the following profile:
            - Age: {age}
            - Has a University Degree: {has_degree}
            - Field of Specialty / Experience: {specialty}
            - Has a Laptop: {have_device_laptop}

            Your job is to help this person build serious wealth from where they are right now.

            Do the following:
            1. Analyse the CURRENT market opportunity in their specialty field (2-3 sentences). What is hot, what pays well, what is growing fast?
            2. Based on their profile and market analysis, give them a brutally honest, actionable, step-by-step roadmap to build wealth.
            3. Each step must be SPECIFIC — not "learn Python", but "spend 2 hours daily on Python via freeCodeCamp for 3 months then build 2 portfolio projects".
            4. Consider their age, whether their degree adds value or they need to self-learn, and whether having no laptop limits them (and how to work around it).
            5. Include income milestones and realistic timelines.

            Format your response EXACTLY like this:

            **Market Opportunity Analysis:**
            [2-3 sentences on current market trends, demand, and earning potential in their field]

            **Your Wealth-Building Roadmap:**
            [One motivating sentence tailored to their profile]

            **Step-by-Step Action Plan:**
            1. [Specific action — include what, how, how long]
            2. [Specific action — include what, how, how long]
            3. [Keep going for 7-10 steps]

            **Income Milestones:**
            - Month 3: [Realistic earning expectation]
            - Month 6: [Realistic earning expectation]
            - Year 1:  [Realistic earning expectation]
            - Year 3:  [Realistic earning expectation]

            **Timeline to First $10,000:**
            [Honest, specific estimate based on their profile]"""

        # ── Call the Gemini REST API ──────────────────────────────────────
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.7,
                "maxOutputTokens": 1024,
            }
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise RuntimeError(
                f"Gemini API error {response.status_code}: {response.text}"
            )

        data = response.json()

        # ── Extract the text ──────────────────────────────────────────────
        try:
            advice = data["candidates"][0]["content"]["parts"][0]["text"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected response structure: {data}") from e

        return advice



if __name__ == "__main__":
    bot_func = BotFunc("tegUsers.db")
    bot_func.create_table()
    print("This is the logic module.")
    # bot_func.delete_user('6666483906')
    print(bot_func.recommend(age=27, has_degree="yes", specialty="Computer Science", have_device_laptop="yes"))