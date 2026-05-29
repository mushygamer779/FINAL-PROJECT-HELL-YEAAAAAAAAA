# 🤖 BOT RIZZLER `☆*:.｡.o(≧▽≦)o.｡.:*☆`

[![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/framework-pyTelegramBotAPI-orange.svg)](https://github.com/eternnoir/pyTelegramBotAPI)
[![Database](https://img.shields.io/badge/database-SQLite3-lightgrey.svg)](https://www.sqlite.org/index.html)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An AI-powered, context-aware Telegram companion that tracks user profiles, handles secure local sessions, and delivers hyper-personalized recommendations directly to your chat.

---

## 🧭 User Journey & Workflow

Getting started as a user is simple. Follow this workflow to get the most out of **Bot Rizzler**:

[ /start ] ──> [ /register ] ──> [ Answer Questionnaire ] ──> [ /recommend ]│└──> [ /profile ] ──> [ /update ]
1. **Initialize:** Activate the bot using `/start`.
2. **Onboard:** Register via `/register` and complete the automated profile questionnaire.
3. **Discover:** Run `/recommend` to receive custom, AI-tailored suggestions based on your profile details.
4. **Manage:** View your configuration using `/profile` or modify your preferences anytime with `/update`.

---

## 🛠️ Project Architecture & Setup

### 📂 Directory Structure
Ensure your local project directory is organized as follows:
```text
📦 BOT-RIZZLER
 ┣ 📂 venv/                 # Virtual environment files
 ┣ 📜 .env                  # Protected environment variables
 ┣ 📜 bot.py                # Main application entry point
 ┣ 📜 database.py           # SQLite database configuration & queries
 ┗ 📜 README.md             # Project documentation
1️⃣ Virtual Environment InitializationOpen PowerShell inside your project root folder and execute the following commands to create and isolate your workspace:PowerShell# 1. Create the virtual environment wrapper
py -m venv venv

# 2. Grant execution permissions for the current PowerShell session
Set-ExecutionPolicy RemoteSigned -Scope Process

# 3. Activate the environment
.\venv\Scripts\Activate.ps1
2️⃣ Package InstallationWith your virtual environment active (venv), install the official runtime dependencies:Bashpip install pyTelegramBotAPI python-dotenv
📌 Note: sqlite3 is a core Python standard library module. It is pre-installed automatically; do not attempt to install it via pip.3️⃣ Environment ConfigurationCreate a .env file in your root folder to securely map your secure tokens.Фрагмент кода# .env Configuration Matrix
TELEGRAM_BOT_TOKEN="your_fallback_telegram_bot_token_here"
AI_API_KEY="your_conversational_ai_api_key_here"
⚠️ Security Warning: Never commit your .env file to public GitHub repositories.📋 Full Command API ReferenceCommandActionScope/startSystem handshake & greeting payload.Public/helpDisplays command definitions and operations documentation.Public/registerTriggers interactive step-by-step profile generation.Guest/loginAuthenticates user credentials against the SQLite instance.Guest/logoutDrops active state handling and terminates current session.Authenticated/profileQueries and displays current user data structures.Authenticated/updateHot-swaps existing profile preferences.Authenticated/recommendParses profile variables through AI engine for customized output.Authenticated/deleteExecutes a hard drop of all user data blocks from storage.Authenticated⚙️ Core Stack OverviewEngine: pyTelegramBotAPI — High-performance, asynchronous-capable wrapper for the official Telegram Bot API.Storage Layer: SQLite3 — Serverless, zero-configuration local relational database.Secret Management: python-dotenv — Parses .env key-value configurations directly into application system environments.🤝 ContributingContributions, issues, and feature requests are welcome! Feel free to check the issues page if you want to expand the Rizzler capabilities.