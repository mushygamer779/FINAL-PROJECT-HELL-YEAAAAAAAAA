# Career Roadmap Telegram Bot

A Telegram bot that collects a user's professional profile and generates a personalized, real-world roadmap for earning their first $100,000 while unemployed. Recommendations are produced by the Google Gemini API and tailored to each user's age, education, field of specialty, available equipment, and self-reported skills.

## Overview

The bot guides each user through a short registration survey, stores their information in a local SQLite database, and lets them request an AI-generated career and income roadmap on demand. Users can also record individual skills (with years of experience and a short description), which are fed into the recommendation to produce more accurate, personalized advice.

The project is split into two modules:

- `main.py` — the Telegram interface layer. Handles commands, the conversational survey flow, and message delivery.
- `logic.py` — the data and AI layer. Manages the SQLite database and the Gemini API request that generates recommendations.

## Features

- User registration through a guided, multi-step survey.
- Persistent storage of user profiles in a local SQLite database.
- Skill tracking, where each user can attach multiple skills, each with a duration and description, stored in a linked table.
- AI-generated career roadmaps based on the full user profile, including all recorded skills.
- Profile management commands to view, update, and delete stored information.
- Output formatted as plain text and length-checked to comply with Telegram's message limits.

## Requirements

- Python 3.10 or newer
- A Telegram bot token from BotFather
- A Google Gemini API key from Google AI Studio

### Python dependencies

- pyTelegramBotAPI
- requests
- python-dotenv

Install them with:

```
pip install pyTelegramBotAPI requests python-dotenv
```

## Configuration

Create a file named `.env` in the project root with the following values:

```
TOKEN=your_telegram_bot_token
GeminiAPI=your_gemini_api_key
```

The `.env` file is loaded automatically at runtime. It should never be committed to version control. Add the following to a `.gitignore` file:

```
.env
__pycache__/
*.pyc
*.db
```

## Database Schema

The application uses a single SQLite database file, `tegUsers.db`, created automatically on first run. It contains two tables.

### tegUsers

Stores one row per registered user.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key, auto-incremented |
| user_id | INTEGER | Telegram user ID, unique |
| username | TEXT | User-provided name |
| age | INTEGER | User age |
| degree_yn | TEXT | Whether the user holds a degree |
| speciality | TEXT | Field of study or experience |
| have_device_laptop | TEXT | Whether the user owns a laptop |
| state | TEXT | Current position in the conversation flow |

### userSkills

Stores one row per skill. Each row links back to a user through `user_id`, allowing a single user to have many skills.

| Column | Type | Description |
| --- | --- | --- |
| id | INTEGER | Primary key, auto-incremented |
| user_id | INTEGER | Foreign key referencing tegUsers.user_id |
| skill | TEXT | Name of the skill |
| forHowLong | TEXT | Years of experience with the skill |
| description | TEXT | Short description of the user's experience |

Both tables are created with `CREATE TABLE IF NOT EXISTS`, so starting the application is sufficient to provision the schema. No manual setup is required.

## Commands

| Command | Description |
| --- | --- |
| /start | Display a welcome message |
| /help | List all available commands |
| /register | Begin the registration survey |
| /addskill | Add a skill with experience and description |
| /recommend | Generate a personalized career roadmap |
| /view | Display the user's stored information |
| /update | Update the user's stored information |
| /delete | Delete the user's profile and all associated skills |

## Conversation Flow

The bot tracks each user's progress through a `state` field stored in the database. A catch-all message handler reads the current state and routes the user's next message accordingly.

Registration advances through the following states: awaiting name, awaiting age, awaiting degree, awaiting specialty, and awaiting device. On completion, the state is set to `Registered`.

Adding a skill advances through three states: awaiting skill, awaiting years of experience, and awaiting description. The skill row is created when the first answer is received and is then completed field by field as the remaining answers arrive. On completion, the state returns to `Registered`, and the user may add additional skills by repeating the command.

## How Recommendations Are Generated

When a registered user runs `/recommend`, the bot retrieves the user's profile and all recorded skills, then constructs a prompt for the Gemini API. The prompt includes the user's age, education, specialty, device availability, and a formatted list of their skills, along with formatting instructions that keep the response within Telegram's character limit and free of markdown symbols.

The request targets the `gemini-2.5-flash` model with internal reasoning disabled, so that the full output budget is spent on the answer itself. The response is parsed defensively: if the model returns no usable text, a descriptive error is raised rather than failing silently. Before being returned, the text is stripped of stray markdown and truncated if necessary to remain within the 4,096-character limit imposed by Telegram.

## Running the Bot

With the environment configured and dependencies installed, start the bot from the project root:

```
python main.py
```

The bot registers its command menu with Telegram and begins long polling. A confirmation message is printed to the console once it is running.

To test the recommendation logic in isolation without launching the full bot, run the logic module directly:

```
python logic.py
```

This executes a sample recommendation call and prints the result.

## Project Structure

```
.
├── main.py          Telegram command handlers and conversation flow
├── logic.py         Database operations and Gemini API integration
├── tegUsers.db      SQLite database (created automatically)
├── .env             Environment variables (not committed)
└── README.md        Project documentation
```

## Notes and Limitations

- The Gemini free tier is subject to regional availability and rate limits. If requests return a quota error with a limit of zero, enabling billing on the associated Google Cloud project, even with a minimal budget alert, typically resolves access.
- Telegram requires all command names to be lowercase. Command identifiers must not contain uppercase characters.
- The database connection is opened with `check_same_thread=False` to support the bot's polling model. For higher-concurrency deployments, a connection-pooling approach is recommended.
- API keys and tokens must be kept private. Any credential that is exposed should be revoked and regenerated immediately.