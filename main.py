import sqlite3 
from telebot import TeleBot
import dotenv
import telebot
import os
from logic import BotFunc 


dotenv.load_dotenv()
bot = TeleBot(os.getenv('TOKEN'))
bot_func = BotFunc("users.db")


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Here are the available commands:' \
                                        '\n/help - Show this help message.' \
                                        '\n/register - Register for the service.' \
                                        '\n/login - Log in to your account.' \
                                        '\n/logout - Log out of your account.' \
                                        '\n/recommend - Get personalized recommendations.' \
                                        '\n/profile - View your profile information.' \
                                        '\n/update - Update your profile information.' \
                                        '\n/delete - Delete your account.')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Welcome to the bot!\nType /help to see available commands.' \
                                      '\nTo get started, you can register an account using /register.')


@bot.message_handler(commands=['register'])
def registration(message):
    bot.send_message(message.chat.id, 'Please enter your username:')
    bot_func.add_user(user_id=message.from_user.id, username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None)

@bot.message_handler(func = lambda message: True)
def forAll(message):
    users = bot_func.get_users()
    print(users)
    for user in users:
        if user[1] == message.from_user.id:  # user[1] is the user_id
            if user[7] == 'Awaiting_Name':
                text = message.text
                bot_func.update_user(user_id=user[1], username=text, status='Awaiting_Age')
                bot.send_message(message.chat.id, 'Please enter your age:')
                continue

            if user[7] == 'Awaiting_Age':
                try:
                    age = int(message.text)
                    pass
                except ValueError:
                    bot.send_message(message.chat.id, 'Invalid input for age. Please enter a valid number:', age)
                    continue
                bot.send_message(message.chat.id, 'Do you have a degree? (Yes/No)')
                continue

            if user[7] == 'Awaiting_Degree':
                bot.send_message(message.chat.id, 'What is your speciality?')
                continue    

            if user[7] == 'Awaiting_Speciality':
                bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No)')
                continue   

            if user[7] == 'Awaiting_Device':
                print(user)
                bot_func.register_user(user_id=user[1], username=user[2], age=user[3], degree_yn=user[4], speciality=user[5], have_device_laptop=user[6])
                bot.send_message(message.chat.id, 'You have successfully registered!\nYour information:\n' \
                                                      f'Username: {user[2]}\n' \
                                                      f'Age: {user[3]}\n' \
                                                      f'Degree: {user[4]}\n' \
                                                      f'Speciality: {user[5]}\n' \
                                                      f'Laptop: {user[6]}')
                bot_func.delete_user(user_id=message.from_user.id)
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


if __name__ == '__main__':
    user = bot_func.get_users()
    print(user)
    bot.infinity_polling()
