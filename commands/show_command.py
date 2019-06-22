from commands.command import Command
from pymongo import MongoClient
from config import config

class ShowCommand(Command):
    def _get_messages(self, message):
        collection = self._get_collection(message)
        messages = self.database[collection] \
            .find({}) \
            .sort([("created_at", -1)]) \
            .limit(10)
        return messages

    def _send_messages(self, message, messages):
        total_message = "Messages from database:\n"
        for saved_message in messages:
            total_message += "{}:\n{}\n\n".format(saved_message["_id"], saved_message["text"])
        self.bot.reply_to(message, total_message)

    def run(self, message):
        messages = self._get_messages(message)
        self._send_messages(message, messages)