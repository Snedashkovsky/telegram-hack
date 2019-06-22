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

    def _get_rating(self, message, message_id):
        collection = self._get_vote_collection(message)
        upvotes = self.database[collection].count({"votee_message": message_id, "vote": 1})
        downvotes = self.database[collection].count({"votee_message": message_id, "vote": -1})
        return {
            "upvotes": upvotes,
            "downvotes": downvotes
        }

    def _get_message_text(self, message, message_from_database):
        message_text = "{}".format(message_from_database["address"])

        message_rating = self._get_rating(message, message_from_database["_id"]) 
        message_text += "\n\nAdded: {date}\n{upvotes} upvotes, {downvotes} downvotes".format(
            date=message_from_database["created_at"].strftime("%y.%m.%d"), 
            **message_rating
        )

        if message_from_database["location"]:
            message_text += "\n\nhttps://maps.google.com/?q={lat},{lng}&mid={message_id}&aid={author_id}".format(
                **message_from_database["location"],
                message_id=message_from_database["_id"], 
                author_id=message_from_database["author"]
            )

        return message_text

    def _send_messages(self, message, messages):
        total_message = "Latest community choice:\n"
        for saved_message in messages:
            saved_message_text = self._get_message_text(message, saved_message)
            self.bot.send_message(
                message.chat.id, 
                saved_message_text
            )

    def run(self, message):
        messages = self._get_messages(message)
        self._send_messages(message, messages)