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
        self.create_skills_table()

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

    def create_skills_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS userSkills (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                user_id INTEGER,
                                skill TEXT,
                                forHowLong TEXT,
                                description TEXT,
                                FOREIGN KEY (user_id) REFERENCES tegUsers(user_id)
                            )''')
        self.conn.commit()

    def start_skill(self, user_id, skill):
        self.cursor.execute('''INSERT INTO userSkills (user_id, skill, forHowLong, description)
                            VALUES (?, ?, NULL, NULL)''', (user_id, skill))
        self.conn.commit()

    def update_latest_skill(self, user_id, forHowLong=None, description=None):
        self.cursor.execute('''SELECT id FROM userSkills WHERE user_id = ? ORDER BY id DESC LIMIT 1''', (user_id,))
        row = self.cursor.fetchone()
        if row:
            skill_id = row[0]
            if forHowLong is not None:
                self.cursor.execute('''UPDATE userSkills SET forHowLong = ? WHERE id = ?''', (forHowLong, skill_id))
            if description is not None:
                self.cursor.execute('''UPDATE userSkills SET description = ? WHERE id = ?''', (description, skill_id))
            self.conn.commit()

    def get_skills(self, user_id):
        self.cursor.execute('SELECT * FROM userSkills WHERE user_id = ?', (user_id,))
        rows = self.cursor.fetchall()
        columns = ['id', 'user_id', 'skill', 'forHowLong', 'description']
        return [dict(zip(columns, row)) for row in rows]

    def delete_skills(self, user_id):
        self.cursor.execute('''DELETE FROM userSkills WHERE user_id = ?''', (user_id,))
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
   

    def recommend(self, age: int, has_degree: str, specialty: str, have_device_laptop: str, user_id: int = None) -> str:
        """
        Generate a Telegram-ready 'first $100k while unemployed' roadmap using the Gemini API.

        Returns clean plain text (no markdown asterisks) that fits within
        Telegram's 4096-character message limit.

        Example:
            >>> print(recommend(27, "yes", "Computer Science", "yes"))
        """

        # ── Load env & build URL ──────────────────────────────────────────
        load_dotenv()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={os.getenv('GeminiAPI')}"

        # ── Normalise inputs ──────────────────────────────────────────────
        has_degree         = str(has_degree).strip().lower()
        have_device_laptop = str(have_device_laptop).strip().lower()
        specialty          = str(specialty).strip()

        # ── Pull the user's saved skills (if any) ─────────────────────────
        skills_block = "They have not listed any extra skills."
        if user_id is not None:
            skills = self.get_skills(user_id)
            lines = []
            for s in skills:
                if s['skill']:  # ignore any half-finished entries
                    lines.append(f"- {s['skill']} | {s['forHowLong']} years | {s['description']}")
            if lines:
                skills_block = "Skills and experience they personally listed:\n" + "\n".join(lines)

        # ── Build the prompt ──────────────────────────────────────────────
        prompt = f"""You are a brutally honest wealth coach and career strategist who has helped thousands of unemployed people earn their first $100,000.

            Here is the person in front of you:
            - Age: {age}
            - Has a University Degree: {has_degree}
            - Field of Specialty / Experience: {specialty}
            - Has a Laptop: {have_device_laptop}

            {skills_block}

            This person is currently UNEMPLOYED and wants a realistic, real-life plan to make their first $100,000 total income. No fluff, no get-rich-quick nonsense. Real, proven paths.

            Tailor everything to their age, degree, specialty, whether they have a laptop, AND the specific skills they listed above. If they listed skills, build the roadmap around their strongest ones.

            IMPORTANT FORMATTING RULES (this will be sent as a plain Telegram message):
            - Do NOT use any markdown, asterisks, bold, or special symbols.
            - Use plain text only. For section titles, just write them on their own line followed by a colon.
            - Use simple numbered lists like "1." for steps.
            - Keep the WHOLE response UNDER 3500 characters so it fits in one Telegram message. Be concise and punchy.

            Structure your answer like this:

            MARKET OPPORTUNITY ANALYSIS:
            [2-3 sentences on what is in demand in {specialty} right now and realistic entry points.]

            YOUR STEP-BY-STEP ROADMAP TO YOUR FIRST 100K:
            1. [Concrete first action - what to do and how.]
            2. [The in-demand skill to learn and a free/cheap resource.]
            3. [Build a portfolio - free/cheap work to prove yourself.]
            4. [Start charging - where to find paying work, what to charge.]
            5. [Scale up - raise rates or move to higher-paying roles.]
            6. [Continue for 7-8 total steps until it realistically reaches 100k.]

            INCOME MILESTONES:
            - First $1,000: [how and when]
            - First $10,000: [how and when]
            - First $100,000: [how and when]

            THE ONE THING THAT MATTERS MOST FOR YOU:
            [One blunt, personalized sentence based on their exact situation.]

            Make sure the whole response is complete and stays under 3500 characters."""

        # ── Call the Gemini REST API ──────────────────────────────────────
        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ],
            "generationConfig": {
                "temperature": 0.8,
                "maxOutputTokens": 4096,
                "thinkingConfig": {
                    "thinkingBudget": 0
                }
            }
        }

        headers = {"Content-Type": "application/json"}

        response = requests.post(url, headers=headers, data=json.dumps(payload))

        if response.status_code != 200:
            raise RuntimeError(
                f"Gemini API error {response.status_code}: {response.text}"
            )

        data = response.json()

        # ── Extract the text (robustly) ───────────────────────────────────
        try:
            candidate = data["candidates"][0]
            parts = candidate.get("content", {}).get("parts")
            if not parts:
                reason = candidate.get("finishReason", "UNKNOWN")
                raise RuntimeError(
                    f"Model returned no text (finishReason={reason}). Full response: {data}"
                )
            advice = parts[0]["text"]
        except (KeyError, IndexError) as e:
            raise RuntimeError(f"Unexpected response structure: {data}") from e

        # ── Make it Telegram-safe ─────────────────────────────────────────
        advice = advice.replace("**", "").replace("__", "").strip()  # strip markdown
        if len(advice) > 4096:                                       # enforce Telegram's hard limit
            advice = advice[:4090].rsplit("\n", 1)[0] + "\n..."

        return advice


if __name__ == "__main__":
    bot_func = BotFunc("tegUsers.db")
    bot_func.create_table()
    print("This is the logic module.")
    # bot_func.delete_user('6666483906')o
    # print(bot_func.recommend(age=27, has_degree="yes", specialty="Computer Science", have_device_laptop="yes"))
    #bot_func.create_skills_table()
    print(bot_func.showAllUsers())