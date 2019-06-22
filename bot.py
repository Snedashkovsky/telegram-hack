import telebot
import os
from config import config
from commands.welcome_command import WelcomeCommand
from commands.save_command import SaveCommand
from commands.show_command import ShowCommand
from commands.vote_command import VoteCommand

bot = telebot.TeleBot(config["BOT_TOKEN"])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    WelcomeCommand(bot).run(message)

@bot.message_handler(commands=['show'])
def show_addresses(message):
    ShowCommand(bot).run(message)

@bot.message_handler(commands=['save'])
def save_address(message):
    SaveCommand(bot).run(message)

@bot.message_handler(regexp='^\\+$')
def vote_address(message):
    VoteCommand(bot).run(message)

@bot.message_handler(regexp='^\\-$')
def unvote_address(message):
    VoteCommand(bot, vote=-1).run(message)

bot.polling()