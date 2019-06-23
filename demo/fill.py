from pymongo import MongoClient
from datetime import datetime
from config import config
from commands.save_command import get_location
import random

addresses = []

def create_address(index, address, author):
    return {
        "_id": "test_{}".format(index),
        "address": address,
        "author": "user_{}".format(author),
        "created_at": datetime.now(),
        "location": get_location(address)
    }

def create_vote(index, voter, votee, vote):
    votee_messages = [address["_id"] for address in addresses if address["author"] == "user_{}".format(votee)]
    random_message = ""
    if votee_messages:
        random_message = random.choice(votee_messages)
    else:
        pass
    return {
        "_id": "test_vote_{}".format(index),
        "voter": "user_{}".format(voter),
        "votee": "user_{}".format(votee),
        "votee_message": random_message,
        "created_at": datetime.now(),
        "vote": vote
    }

def save(collection, items):
    client = MongoClient(config["MONGO_HOST"])
    for item in items:
        client[config["MONGO_DATABASE"]][collection].update({
            "_id": item["_id"]
        }, {
            "$set": item
        }, upsert=True)

def fill():
    addresses.append(create_address(0, "Минск, Имагуру", 1))
    addresses.append(create_address(1, "Минск, President Hotel", 2))
    addresses.append(create_address(2, "Минск, бар Чердак", 3))

    votes = [
        create_vote(0, 1, 2, 1),
        create_vote(1, 2, 1, 1),
        create_vote(2, 3, 1, 1),
        create_vote(3, 4, 2, 1),
        create_vote(4, 5, 2, 1),
        create_vote(41, 1, 4, 1),
        create_vote(5, 3, 5, 1),
        create_vote(6, 3, 6, 1),
        create_vote(7, 3, 7, 1),
        create_vote(8, 3, 8, 1),
        create_vote(9, 8, 1, 1),
        create_vote(10, 8, 7, 1),
        create_vote(11, 7, 6, 1),
        create_vote(12, 1, 3, 1),
        create_vote(13, 1, 8, 1),

        # User 10 is fucked

        create_vote(14, 10, 11, 1),
        create_vote(15, 11, 10, 1),
        create_vote(16, 10, 12, 1),
        create_vote(17, 12, 10, 1),

        create_vote(18, 1, 10, -1),
        create_vote(19, 2, 10, -1),
        create_vote(20, 3, 10, -1),
    ]

    save(config["TEST_MONGO_COLLECTION"], addresses)
    save(config["TEST_MONGO_COLLECTION"] + "_votes", votes)