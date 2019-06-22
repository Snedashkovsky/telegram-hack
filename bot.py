import telebot
import os
from config import config
from commands.welcome_command import WelcomeCommand
from commands.save_command import SaveCommand

bot = telebot.TeleBot(config["BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    WelcomeCommand(bot).run(message)

@bot.message_handler(commands=['show'])
def show_messages(message):
    ShowCommand(bot).run(message)
    # Get N from message
    # Show latest N messages

@bot.message_handler(commands=['delete'])
def delete_messages(message):
    DeleteCommand(bot).run(message)
    # Delete message with id from mongo

@bot.message_handler(func=lambda message: True)
def save_message(message):
    SaveCommand(bot).run(message)

bot.polling()