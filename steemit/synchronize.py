from time import sleep
from tqdm import tqdm
from pymongo import MongoClient
from steemit.steemit_client import SteemitClient
from config import config
import json
from bson import json_util


steemit_client = SteemitClient()
mongo_client = MongoClient(config["MONGO_HOST"])
mongo_database = mongo_client[config["MONGO_DATABASE"]]

def get_collections():
    return config["TEST_MONGO_COLLECTION"], config["TEST_MONGO_COLLECTION"] + "_votes"

def get_latest_posts_from_steemit():
    return steemit_client.get_posts()

def save_items_to_mongo(collection, items):
    for item in items:
        item_body = json.loads(item["body"], object_hook=json_util.object_hook)

        mongo_database[collection].update({
            "_id": item_body["_id"]
        }, {
            "$set": item_body
        }, upsert=True)

def split_votes_and_messages(all_messages):
    return ...

if (__name__ == "__main__"):
    messages_collection, votes_collection = get_collections()
    all_messages = get_latest_posts_from_steemit()
    messages, votes = split_votes_from_messages(all_messages)
    save_items_to_mongo(messages_collection, messages)
    save_items_to_mongo(votes_collection, votes)