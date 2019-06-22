from time import sleep
from tqdm import tqdm
from pymongo import MongoClient
# from steemit.steemit_client import SteemitClient
from config import config

STEEMIT_FIELD = "synchronized"

# steemit_client = SteemitClient()
mongo_client = MongoClient(config["MONGO_HOST"])
mongo_database = mongo_client[config["MONGO_DATABASE"]]

def get_collections():
    return mongo_database.collection_names()

def get_collections_content(collections):
    items = []
    for collection in collections:
        items += list(mongo_database[collection].find({ 
            STEEMIT_FIELD: { 
                "$exists" : False 
            }
        }))
    return items

def get_latest_messages(collections):
    collections = [collection for collection in collections if not collection.endswith("votes")]
    return get_collections_content(collections)

def get_latest_votes(collections):
    collections = [collection for collection in collections if collection.endswith("votes")]
    return get_collections_content(collections)

def mark_everything_as_processed(collections):
    for collection in collections:
        mongo_database[collection].update_many({}, {
            "$set": {
                STEEMIT_FIELD: True
            }
        })

def send_message_to_steemit(message):
    print(message)

def send_vote_to_steemit(vote):
    print(vote)

if (__name__ == "__main__"):
    collections = get_collections()
    messages = get_latest_messages(collections)
    votes = get_latest_votes(collections)

    mark_everything_as_processed(collections)

    for message in tqdm(messages):
        send_message_to_steemit(message)

    for vote in tqdm(votes):
        send_vote_to_steemit(vote)

    # sleep(10)