from time import sleep
from tqdm import tqdm
from pymongo import MongoClient
from blockchains.steemit_client import SteemitClient
from blockchains.fluence_client import FluenceClient
from config import config
import json
from bson import json_util

def get_steemit_client():
    return SteemitClient(config["STEEMIT_ACCOUNT"], config["STEEMIT_KEY"])

def get_fluence_client():
    return FluenceClient() 

def get_client(name):
    return {
        "steemit": get_steemit_client,
        "fluence": get_fluence_client
    }[name]


blockchain_client = get_client(config["BLOCKCHAIN_CLIENT"])()
mongo_client = MongoClient(config["MONGO_HOST"])
mongo_database = mongo_client[config["MONGO_DATABASE"]]

def get_collections():
    return config["TEST_MONGO_COLLECTION"], config["TEST_MONGO_COLLECTION"] + "_votes"

def get_latest_posts_from_blockchain():
    return blockchain_client.get_posts(config["TEST_STEEMIT_PARENT"])

def save_items_to_mongo(collection, items):
    for item in items:
        try:
            item_body = json.loads(item, object_hook=json_util.object_hook)
        except: 
            continue

        mongo_database[collection].update({
            "_id": item_body["_id"]
        }, {
            "$set": item_body
        }, upsert=True)

def synchronize():
    messages_collection, votes_collection = get_collections()
    messages, votes = get_latest_posts_from_blockchain()
    save_items_to_mongo(messages_collection, messages)
    save_items_to_mongo(votes_collection, votes)    