import sqlite3 
from telebot import TeleBot
import dotenv
import os

dotenv.load_dotenv()
bot = TeleBot(os.getenv('TOKEN'))


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
    bot.send_message(message.chat.id, 'Welcome to the bot! Type /help to see available commands.' \
                                      '\nTo get started, you can register an account using /register.')

@bot.message_handler(func = lambda message: True)
def forAll(message):
    bot.send_message(message.chat.id, 'hello, world!')


bot.infinity_polling()

if __name__ == '__main__':
    print("Bot is running...")