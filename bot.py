import telebot
import os
from config import config
from commands.welcome_command import WelcomeCommand
from commands.save_command import SaveCommand
from commands.show_command import ShowCommand

bot = telebot.TeleBot(config["BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    WelcomeCommand(bot).run(message)

@bot.message_handler(commands=['show'])
def show_messages(message):
    ShowCommand(bot).run(message)

@bot.message_handler(commands=['save'])
def save_message(message):
    SaveCommand(bot).run(message)

bot.polling()