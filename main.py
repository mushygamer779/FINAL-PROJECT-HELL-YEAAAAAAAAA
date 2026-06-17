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
                                      '/AddSkill - Add a skill you have\n'
                                      '/delete - Delete your information\n'
                                      '/view - View your information\n'
                                      '/update - Update your information\n'
                                      '/help - Show this help message')

ifStart = True
@bot.message_handler(commands=['start'])
def start(message):
    if ifStart:
        bot.send_message(message.chat.id, 'Welcome to the bot!\nType /help to see available commands.' \
                                      '\nTo get started, you can register an account using /register.')
        ifStart = False

@bot.message_handler(commands=['register'])
def registration(message):
    users = bot_logic.showAllUsers()
    for user in users: 
        if user['user_id'] == message.from_user.id:
            bot.send_message(message.chat.id, 'You are already registered! Use /update to change your information.')
            return
    bot.send_message(message.chat.id, 'You are not registered yet. Please follow the prompts to register.')
    bot.send_message(message.chat.id, 'Please enter your username:') 
    bot_logic.register_user(user_id=message.from_user.id, username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Awaiting_Name')


@bot.message_handler(commands=['recommend'])
def recommend(message):
    users = bot_logic.showAllUsers()
    for User in users:
        if User['user_id'] == message.from_user.id:
            if User['state'] != 'Registered':
                bot.send_message(message.chat.id, 'Please complete your registration first using /register.')
                return
            else:
                recommendation = bot_logic.recommend(age=User['age'], has_degree=User['degree_yn'], specialty=User['speciality'], have_device_laptop=User['have_device_laptop'], user_id=User['user_id'])
                bot.send_message(message.chat.id, f'Based on your information here is the recommendation:\n{recommendation}')
                return



@bot.message_handler(commands=['view'])
def view(message):
    users = bot_logic.showAllUsers()
    for User in users:
        if User['user_id'] == message.from_user.id:
            if User['state'] != 'Registered':
                bot.send_message(message.chat.id, 'Please complete your registration first using /register.')
                return
            else:
                bot.send_message(message.chat.id, f'Here is your current information:\n'
                                                   f'Age: {User["age"]}\n'
                                                   f'Has Degree: {User["degree_yn"]}\n'
                                                   f'Specialty: {User["speciality"]}\n'
                                                   f'Have Laptop: {User["have_device_laptop"]}')
                return
            

@bot.message_handler(commands=['update'])
def update(message):
    users = bot_logic.showAllUsers()
    for User in users:
        if User['user_id'] == message.from_user.id:
            if User['state'] != 'Registered':
                bot.send_message(message.chat.id, 'Please complete your registration first using /register.')
                return
            else:
                bot.send_message(message.chat.id, 'To update your information, please follow the prompts.')
                bot.send_message(message.chat.id, 'Please enter your new username (or type "skip" to keep current):')
                bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Updating_Name')
                return


@bot.message_handler(commands=['delete'])
def delete(message):
    users = bot_logic.showAllUsers()
    for User in users:
        if User['user_id'] == message.from_user.id:
            bot_logic.delete_user(User['user_id'])
            bot_logic.delete_skills(User['user_id'])
            bot.send_message(message.chat.id, 'Your information has been deleted. Use /register to sign up again.')
            return
    bot.send_message(message.chat.id, 'You are not registered, so there is nothing to delete.')


@bot.message_handler(commands=['addSkill'])
def addSkill(message):
    users = bot_logic.showAllUsers()
    for User in users:
        if User['user_id'] == message.from_user.id:
            if User['state'] != 'Registered':
                bot.send_message(message.chat.id, 'Please complete your registration first using /register.')
                return
            else:
                bot.send_message(message.chat.id, 'What skill do you have? (e.g. Python, Graphic Design)')
                bot_logic.update_user(user_id=User['user_id'], state='Awaiting_Skill')
                return
    bot.send_message(message.chat.id, 'You are not registered yet. Use /register first.')


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
                    if int(message.text) <= 0 or int(message.text) < 6:
                        bot.send_message(message.chat.id, 'fetus cant type. Please enter a valid age:')
                        continue
                    elif int(message.text) > 120:
                        bot.send_message(message.chat.id, 'how are you still jobless? Please enter a valid age:')
                        continue
                    else:
                        bot_logic.update_user(user_id=User['user_id'], username=None, age=int(message.text), degree_yn=None, speciality=None, have_device_laptop=None, state='Awaiting_Degree')
                        
                except ValueError:
                    bot.send_message(message.chat.id, 'Invalid input for age. Please enter a valid number:')
                    continue
                
                bot.send_message(message.chat.id, 'Do you have a degree? (Yes/No)')
                continue

            if User['state'] == 'Awaiting_Degree':
          
                if message.text.lower() not in ['yes', 'no', 'yea', 'ye', 'yez', 'na', 'nah']:
                    bot.send_message(message.chat.id, 'Yes or no?')
                    continue
                else: 
                    if message.text.lower() in ['yes', 'yea', 'ye', 'yez']:
                        bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn='yes', speciality=None, have_device_laptop=None, state='Awaiting_Speciality')
                        bot.send_message(message.chat.id, 'What is your speciality?')
                        continue    
                    elif message.text.lower() in ['no', 'na', 'nah']:
                        bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn='no', speciality='None', have_device_laptop=None, state='Awaiting_Device')
                        bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No)')
                        continue   

            if User['state'] == 'Awaiting_Speciality':
                bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=message.text, have_device_laptop=None, state='Awaiting_Device')
                bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No)')
                continue   

            if User['state'] == 'Awaiting_Device':
                if message.text.lower() not in ['yes', 'no', 'yea', 'ye', 'yez', 'na', 'nah']:
                    bot.send_message(message.chat.id, 'Yes or no?')
                    continue
                else: 
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

            if User['state'] == 'Awaiting_Skill':
                bot_logic.start_skill(User['user_id'], message.text)
                bot_logic.update_user(user_id=User['user_id'], state='Awaiting_SkillYears')
                bot.send_message(message.chat.id, 'How many years of experience do you have with it?')
                continue

            if User['state'] == 'Awaiting_SkillYears':
                bot_logic.update_latest_skill(User['user_id'], forHowLong=message.text)
                bot_logic.update_user(user_id=User['user_id'], state='Awaiting_SkillDesc')
                bot.send_message(message.chat.id, 'Briefly describe your experience with it:')
                continue

            if User['state'] == 'Awaiting_SkillDesc':
                bot_logic.update_latest_skill(User['user_id'], description=message.text)
                bot_logic.update_user(user_id=User['user_id'], state='Registered')
                bot.send_message(message.chat.id, 'Skill added! Use /AddSkill again to add another, or /recommend to get your roadmap.')
                continue

            if User['state'] == 'Updating_Name':
                bot_logic.update_user(user_id=User['user_id'], username=message.text if message.text.lower() != 'skip' else None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Updating_Age')
                bot.send_message(message.chat.id, 'Please enter your new age (or type "skip" to keep current):')
                continue
            if User['state'] == 'Updating_Age':
                if message.text.lower() != 'skip':
                    try:
                        if int(message.text) <= 0 or int(message.text) < 6:
                            bot.send_message(message.chat.id, 'fetus cant type. Please enter a valid age:')
                            continue
                        elif int(message.text) > 120:
                            bot.send_message(message.chat.id, 'how are you still jobless? Please enter a valid age:')
                            continue
                        else:
                            bot_logic.update_user(user_id=User['user_id'], username=None, age=int(message.text), degree_yn=None, speciality=None, have_device_laptop=None, state='Updating_Degree')
                    except ValueError:
                        bot.send_message(message.chat.id, 'Invalid input for age. Please enter a valid number:')
                        continue
                else:
                    bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=None, state='Updating_Degree')
                bot.send_message(message.chat.id, 'Do you have a degree? (Yes/No or "skip")')
                continue
            if User['state'] == 'Updating_Degree':
                if message.text.lower() not in ['yes', 'no', 'yea', 'ye', 'yez', 'na', 'nah', 'skip']:
                    bot.send_message(message.chat.id, 'Yes or no? (or "skip")')
                    continue
                else: 
                    bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=message.text if message.text.lower() != 'skip' else None, speciality=None, have_device_laptop=None, state='Updating_Speciality')
                    bot.send_message(message.chat.id, 'What is your speciality? (or "skip")')
                    continue
            if User['state'] == 'Updating_Speciality':
                bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=message.text if message.text.lower() != 'skip' else None, have_device_laptop=None, state='Updating_Device')
                bot.send_message(message.chat.id, 'Do you have a laptop? (Yes/No or "skip")')
                continue                       

            if User['state'] == 'Updating_Device':
                if message.text.lower() not in ['yes', 'no', 'yea', 'ye', 'yez', 'na', 'nah', 'skip']:
                    bot.send_message(message.chat.id, 'Yes or no? (or "skip")')
                    continue
                else: 
                    bot_logic.update_user(user_id=User['user_id'], username=None, age=None, degree_yn=None, speciality=None, have_device_laptop=message.text if message.text.lower() != 'skip' else None, state='Registered')
                    updated = next(u for u in bot_logic.showAllUsers() if u['user_id'] == message.from_user.id)
                    bot.send_message(message.chat.id,
                        'Your information has been updated!\nYour current information:\n'
                        f'Username: {updated["username"]}\n'
                        f'Age: {updated["age"]}\n'
                        f'Degree: {updated["degree_yn"]}\n'
                        f'Speciality: {updated["speciality"]}\n'
                        f'Laptop: {updated["have_device_laptop"]}'
                    )
                    continue



# bot.delete_my_commands(scope=None, language_code=None)

# bot.set_my_commands(
#     commands= [
#         telebot.types.BotCommand("/start","start bot"),
#         telebot.types.BotCommand("/register","register user"),
#         telebot.types.BotCommand("/recommend","Reconmendation for JOBLESS"),
#         telebot.types.BotCommand("/addSkill","add a skill you have"),
#         telebot.types.BotCommand("/view","view info"),
#         telebot.types.BotCommand("/delete","delete info"),
#         telebot.types.BotCommand("/update","update info"),
#         telebot.types.BotCommand("/help","help")
#             ],
#         scope=None, language_code=None
# )

# # check command
# cmd = bot.get_my_commands(scope=None, language_code=None)
# print([c.to_json() for c in cmd])

if __name__ == '__main__':
    print("Bot is running...")
    bot.infinity_polling()
