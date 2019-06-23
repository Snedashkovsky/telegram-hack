from pymongo import MongoClient
from steemit.steemit_client import SteemitClient
from config import config
import json
from bson import json_util

class Command():
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(config["MONGO_HOST"])
        self.steemit_client = SteemitClient(config["STEEMIT_ACCOUNT"], config["STEEMIT_KEY"])
        self.database = self.client[config["MONGO_DATABASE"]]

    def _get_collection(self, message):
        return config["TEST_MONGO_COLLECTION"]
        # return "collection_{}".format(message.chat.id)

    def _get_vote_collection(self, message):
        return "{}_{}".format(self._get_collection(message), "votes")

    def _get_author(self, message):
        return "user_{}".format(message.from_user.id)

    def _get_message_id(self, message):
        return "{}_{}".format(message.chat.id, message.message_id)

    def _save_to_steemit(self, message_dict, parent_link=""):
        parent_link = "{}/{}".format(config["TEST_STEEMIT_PARENT"], parent_link)
        self.steemit_client.send_low_level_post(
            author=config["STEEMIT_ACCOUNT"],
            title=message_dict["_id"],
            body=json.dumps(message_dict, default=json_util.default),
            parent_link=parent_link
        )

    def _save_to_mongo(self, message, message_dict, collection=None):
        if not collection:
            collection = self._get_collection(message)
        self.database[collection].save(message_dict)