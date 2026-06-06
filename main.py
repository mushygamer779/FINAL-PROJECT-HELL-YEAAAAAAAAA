import sqlite3 
from telebot import TeleBot
import dotenv
import telebot
import os
from logic import BotFunc


dotenv.load_dotenv()
bot = TeleBot(os.getenv('TOKEN'))


bot_logic = BotFunc('users.db')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Available commands:\n'
                                      '/start - Start the bot\n'
                                      '/register - Register an account\n'
                                      '/recommend - Get job recommendations\n'
                                      '/view - View your information\n'
                                      '/delete - Delete your information\n'
                                      '/update - Update your information\n'
                                      '/help - Show this help message')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome to the bot!\nType /help to see available commands.' \
                                      '\nTo get started, you can register an account using /register.')


@bot.message_handler(commands=['register'])
def registration(message):
    users = []
    bot.send_message(message.chat.id, 'Please enter your username:')
    bot_logic.register_user(user_id=message.from_user.id, username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Awaiting_Name')


@bot.message_handler(func = lambda message: True)
def forAll(message):
    global Users
    for User in Users:
        if User['UserID'] == message.from_user.id:

            if User['State'] == 'Awaiting_Name':
                User['User_Name'] = message.text
                User['State'] = 'Awaiting_Age'
                bot.send_message(message.chat.id, 'Please enter your age:')
                continue

            if User['State'] == 'Awaiting_Age':
                try:
                    User['Age'] = int(message.text)
                except ValueError:
                    bot.send_message(message.chat.id, 'Invalid input for age. Please enter a valid number:')
                    continue
                User['State'] = 'Awaiting_Degree'
                bot.send_message(message.chat.id, 'Do you have a degree? (Yes/No)')
                continue

            if User['State'] == 'Awaiting_Degree':
                User['degree_YN'] = message.text
                User['State'] = 'Awaiting_Speciality'
                bot.send_message(message.chat.id, 'What is your speciality?')
                continue    

            if User['State'] == 'Awaiting_Speciality':
                User['Speciality'] = message.text
                User['State'] = 'Awaiting_Device'
                bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No)')
                continue   

            if User['State'] == 'Awaiting_Device':
                User['Have_Device_Laptop'] = message.text
                User['State'] = 'Registered'
                print(User)
                bot_logic.register_user(user_id=User['UserID'], username=User['User_Name'], age=User['Age'], degree_yn=User['degree_YN'], speciality=User['Speciality'], have_device_laptop=User['Have_Device_Laptop'])
                bot.send_message(message.chat.id, 'You have successfully registered!\nYour information:\n' \
                                                      f'Username: {User["User_Name"]}\n' \
                                                      f'Age: {User["Age"]}\n' \
                                                      f'Degree: {User["degree_YN"]}\n' \
                                                      f'Speciality: {User["Speciality"]}\n' \
                                                      f'Laptop: {User["Have_Device_Laptop"]}')
                Users.remove(User)
                continue

bot.delete_my_commands(scope=None, language_code=None)

bot.set_my_commands(
    commands= [
        telebot.types.BotCommand("/start","start bot"),
        telebot.types.BotCommand("/register","register user"),
        telebot.types.BotCommand("/recommend","Reconmendation for JOBLESS"),
        telebot.types.BotCommand("/view","view info"),
        telebot.types.BotCommand("/delete","delete info"),
        telebot.types.BotCommand("/update","update info"),
        telebot.types.BotCommand("/help","help")
            ],
        scope=None, language_code=None
)

# check command
cmd = bot.get_my_commands(scope=None, language_code=None)
print([c.to_json() for c in cmd])

bot.infinity_polling()

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()