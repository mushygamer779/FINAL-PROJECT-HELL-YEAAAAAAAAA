# Career Roadmap Telegram Bot

This is a Telegram bot that gives you a personalized, no-nonsense plan for making your first $100,000 while you're unemployed. You tell it a bit about yourself, and it uses Google's Gemini AI to write a roadmap built around your actual situation: your age, whether you have a degree, what you're good at, whether you own a laptop, and any skills you've picked up along the way.

The idea is simple. Generic career advice is useless because it ignores who you actually are. So this bot collects the details that matter, remembers them, and feeds them to the AI so the advice is genuinely about you.

## How it's put together

The code lives in two files, each with a clear job:

- `main.py` is everything the user touches. It handles the commands, walks people through the questions, and sends messages back.
- `logic.py` is the brain behind the scenes. It talks to the database and to the Geminsi API.

Keeping them separate means you can mess with the conversation flow without touching the AI logic, and vice versa.

## What it can do

- Walk a new user through registration one question at a time.
- Remember everyone's profile in a local database, so it's all still there next time.
- Let users add as many skills as they want, each with how long they've done it and a short description.
- Generate a full career roadmap from the AI that actually takes those skills into account.
- Let people view, update, or delete their info whenever they like.
- Keep the AI's reply clean and short enough that Telegram will actually send it.

## What you'll need

- Python 3.10 or newer
- A Telegram bot token (you get this from BotFather)
- A Google Gemini API key (grab one from Google AI Studio)

You'll also need three Python packages:

- pyTelegramBotAPI
- requests
- python-dotenv

Install them in one go:

```
pip install pyTelegramBotAPI requests python-dotenv
```

## Setting it up

Make a file called `.env` in the project folder and drop your two keys in it:

```
TOKEN=your_telegram_bot_token
GeminiAPI=your_gemini_api_key
```

The bot reads this file automatically when it starts. One important thing: never commit this file to GitHub. Those keys are basically passwords. Make a `.gitignore` and add these lines so you don't leak anything by accident:

```
.env
__pycache__/
*.pyc
*.db
```

## The database

Everything is stored in a single SQLite file called `tegUsers.db`. You don't have to create it yourself. The bot builds it the first time it runs. There are two tables inside.

### tegUsers

One row for each person who registers.

| Column | Type | What it holds |
| --- | --- | --- |
| id | INTEGER | The primary key, counts up on its own |
| user_id | INTEGER | The person's Telegram ID, has to be unique |
| username | TEXT | The name they gave |
| age | INTEGER | Their age |
| degree_yn | TEXT | Whether they have a degree |
| speciality | TEXT | Their field or area of experience |
| have_device_laptop | TEXT | Whether they own a laptop |
| state | TEXT | Where they currently are in the conversation |

### userSkills

One row per skill. Each skill points back to its owner through `user_id`, which is what lets a single person have a whole list of skills.

| Column | Type | What it holds |
| --- | --- | --- |
| id | INTEGER | The primary key, counts up on its own |
| user_id | INTEGER | Links the skill back to a user in tegUsers |
| skill | TEXT | The name of the skill |
| forHowLong | TEXT | How many years they've done it |
| description | TEXT | A quick note about their experience |

Both tables are created with `CREATE TABLE IF NOT EXISTS`, which is a fancy way of saying the bot only makes them if they aren't already there. So just starting the bot is enough. There's nothing to set up by hand.

## The commands

| Command | What it does |
| --- | --- |
| /start | Says hello |
| /help | Lists everything you can do |
| /register | Starts the sign-up questions |
| /addskill | Adds a skill, with experience and a description |
| /recommend | Generates your personalized roadmap |
| /view | Shows you what the bot has stored about you |
| /update | Lets you change your stored info |
| /delete | Wipes your profile and all your skills |

## How the conversation actually works

The bot keeps track of where each person is using a `state` value saved in the database. There's one handler that catches every message, checks what state you're in, and figures out what your message means based on that.

Registration moves through a series of steps: name, then age, then degree, then specialty, then laptop. Once you've answered them all, your state flips to `Registered` and you're done.

Adding a skill works the same way but in three steps: the skill itself, then how many years, then a description. Here's the slightly clever part: the moment you type the skill name, the bot creates the row in the database, then fills in the other two answers as they come in. When it's finished, you go back to `Registered`, and you can run the command again to add another skill whenever you want.

## How the roadmap gets made

When a registered user runs `/recommend`, the bot pulls up their profile and every skill they've saved, then builds a prompt for the Gemini API. That prompt includes their age, education, specialty, whether they have a laptop, and a tidy list of their skills, plus some instructions telling the AI to keep the reply short and skip the markdown symbols (Telegram doesn't love those).

The request goes to the `gemini-2.5-flash` model with its internal "thinking" turned off. That last part matters: this model can spend its whole word budget reasoning to itself and leave nothing for the actual answer, so switching that off makes sure all of it goes into the response you actually see.

The reply is then handled carefully. If the AI sends back nothing usable, the bot raises a clear error instead of crashing in some confusing way. Before the text goes out, any leftover markdown is stripped off and the message is trimmed if it's too long, so it always stays under Telegram's 4,096-character ceiling.

## Running it

Once your keys are in place and the packages are installed, start the bot from the project folder:

```
python main.py
```

It'll register its command menu with Telegram, start listening, and print a message to your console letting you know it's alive.

If you just want to test the AI part on its own without firing up the whole bot, you can run the logic file directly:

```
python logic.py
```

That makes one sample recommendation and prints it out, which is handy for quick checks.

## What's where

```
.
├── main.py          The Telegram side: commands and conversation
├── logic.py         The database and the Gemini API calls
├── tegUsers.db      The SQLite database (made automatically)
├── .env             Your secret keys (never commit this)
└── README.md        You're reading it
```

## A few things worth knowing

- Gemini's free tier isn't available everywhere, and it has rate limits. If you ever get a quota error that says your limit is zero, turning on billing for your Google Cloud project usually fixes it. You can set a tiny budget alert so you're never actually charged for normal use.
- Telegram is picky about command names: they have to be all lowercase. No capital letters allowed, which is why it's `/addskill` and not `/AddSkill`.
- The database connection uses `check_same_thread=False` so it plays nicely with the bot's polling. If you ever scale this up to handle a lot of users at once, you'd want to look into proper connection pooling.
- Keep your keys to yourself. If one ever slips out, revoke it and make a new one right away. It only takes a second and it'll save you a headache.