import sqlite3 
from telebot import TeleBot
import dotenv
import telebot
import os
from logic import BotFunc as BotFunc


dotenv.load_dotenv()
bot = TeleBot(os.getenv('TOKEN'))


bot_logic = BotFunc('tegUsers.db')


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
    users = bot_logic.showAllUsers()
    for user in users: 
        if user['user_id'] == message.from_user.id:
            bot.send_message(message.chat.id, 'You are already registered! Use /update to change your information.')
            return
        else:
            bot.send_message(message.chat.id, 'You are not registered yet. Please follow the prompts to register.')
            bot.send_message(message.chat.id, 'Please enter your username:') 
@bot.message_handler(func = lambda message: True)
def forAll(message):
    global bot_logic
    users = bot_logic.showAllUsers()

    for User in users:
        if User['user_id'] == message.from_user.id:
            if User['state'] == 'Awaiting_Name':
                bot_logic.update_user(user_id=User['user_id'], username=message.text, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Awaiting_Age')
                bot.send_message(message.chat.id, 'Please enter your age:')
                continue
            
            if User['state'] == 'Awaiting_Age':
                try:
                    bot_logic.update_user(user_id=User['user_id'], username=None, age=int(message.text), degree_yn=None, speciality=None, have_device_laptop=None, state='Awaiting_Degree')
                except ValueError:
                    bot.send_message(message.chat.id, 'Invalid input for age. Please enter a valid number:')
                    continue
                
                bot.send_message(message.chat.id, 'Do you have a degree? (Yes/No)')
                continue

            if User['state'] == 'Awaiting_Degree':
                bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=message.text, speciality=None, have_device_laptop=None, state='Awaiting_Speciality')
                bot.send_message(message.chat.id, 'What is your speciality?')
                continue    

            if User['state'] == 'Awaiting_Speciality':
                bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=message.text, have_device_laptop=None, state='Awaiting_Device')
                bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No)')
                continue   

            if User['state'] == 'Awaiting_Device':
                bot_logic.update_user(user_id=User['user_id'], have_device_laptop=message.text, state='Registered')
                # Re-fetch the now-complete user record
                updated = next(u for u in bot_logic.showAllUsers() if u['user_id'] == message.from_user.id)
                bot.send_message(message.chat.id,
                    'You have successfully registered!\nYour information:\n'
                    f'Username: {updated["username"]}\n'
                    f'Age: {updated["age"]}\n'
                    f'Degree: {updated["degree_yn"]}\n'
                    f'Speciality: {updated["speciality"]}\n'
                    f'Laptop: {updated["have_device_laptop"]}'
                )
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