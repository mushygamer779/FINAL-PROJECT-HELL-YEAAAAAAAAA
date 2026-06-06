# BOT RIZZLER ☆*:.｡.o(≧▽≦)o.｡.:*☆

Welcome to **BOT RIZZLER**! Below you will find the available commands, required libraries, and setup instructions to get everything running smoothly.

---

## Available Commands

| Command | Description |
| :--- | :--- |
| `/help` | Show this help message. |
| `/register` | Register for the service. |
| `/login` | Log in to your account. |
| `/logout` | Log out of your account. |
| `/recommend` | Get personalized recommendations. |
| `/profile` | View your profile information. |
| `/update` | Update your profile information. |
| `/delete` | Delete your account. |

---

## Libraries Used

Run the following commands to install the required dependencies:

```bash
pip install PytelegramBotAPI
pip install Sqlite3
pip install dotenv
How to Use
Use /Start

Register using /register

Answer the questionnaire / complete registration

Use /recommend to get recommended something

Use /update to update info about you and use /info to check info about yourself

More SetUp
.env Configuration
Create a .env file in your project root directory.

Save your Bot token and your Api key for chat bot inside the file. : Like this : TOKEN = 'BOT-TOKEN-HERE'

SetUp Digital Environment
Execute these commands in order to set up your virtual environment:

PowerShell
# 1. Create the virtual environment
py -m venv venv

# 2. Set the execution policy for the process
Set-ExecutionPolicy RemoteSigned -Scope Process

# 3. Activate the virtual environment
.\venv\Scripts\Activate.ps1