from pymongo import MongoClient
from config import config

class Command():
    def __init__(self, bot):
        self.bot = bot
        self.client = MongoClient(config["MONGO_HOST"])
        self.database = self.client[config["MONGO_DATABASE"]]
