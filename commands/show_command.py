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
        total_message = "Latest community choice:\n"
        for saved_message in messages:
            self.bot.send_message(
                message.chat.id, 
                saved_message["address"]
            )
            if saved_message["location"]:
                self.bot.send_location(
                    message.chat.id, 
                    saved_message["location"]["lat"], 
                    saved_message["location"]["lng"]
                )

    def run(self, message):
        messages = self._get_messages(message)
        self._send_messages(message, messages)