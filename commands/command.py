from pymongo import MongoClient
from config import config

class Command():
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(config["MONGO_HOST"])
        self.database = self.client[config["MONGO_DATABASE"]]

    def _get_collection(self, message):
        return "collection_{}".format(message.chat.id)

    def _get_author(self, message):
        return "user_{}".format(message.from_user.id)

    def _get_message_id(self, message):
        return "{}_{}".format(message.chat.id, message.message_id)