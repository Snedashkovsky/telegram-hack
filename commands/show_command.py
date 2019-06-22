from commands.command import Command
from pymongo import MongoClient
from config import config

class ShowCommand():
    def _get_messages(self, message):
        collection = self._extract_collection(message)
        messages = self.database[collection].find({
        }).sort({
            "created_at": -1
        }).limit(10)

    def _send_messages(message, messages):
        total_message = "Messages in database:\n"
        for message in messages:
            total_message += "{}. {}\n".format(message["id"], message["text"])
        self.bot.reply_to(message, total_message)

    def run(self, message):
        messages = self._get_messages(message)
        self._send_messages(message, messages)