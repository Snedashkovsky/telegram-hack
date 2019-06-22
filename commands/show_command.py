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

    def _get_message_text(self, message):
        message_text = "{}".format(message["address"])

        if message["location"]:
            message_text += "\n\nhttps://maps.google.com/?q={lat},{lng}&mid={message_id}&aid={author_id}".format(
                **message["location"],
                message_id=message["_id"], 
                author_id=message["author"]
            )

        return message_text

    def _send_messages(self, message, messages):
        total_message = "Latest community choice:\n"
        for saved_message in messages:
            saved_message_text = self._get_message_text(saved_message)
            self.bot.send_message(
                message.chat.id, 
                saved_message_text
            )

    def run(self, message):
        messages = self._get_messages(message)
        self._send_messages(message, messages)