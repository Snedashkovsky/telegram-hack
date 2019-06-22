from time import sleep
from tqdm import tqdm
from steemit.steemit_client import SteemitClient
from config import config

steemit_client = SteemitClient()
mongo_client = PyMongo()

def get_latest_messages():
    pass

def get_latest_votes():
    pass

def mark_as_processed():
    pass

def send_message_to_steemit(message):
    print(messages)

def send_vote_to_steemit(vote):
    print(vote)

if (__name__ == "__main__"):
    messages = get_latest_messages()
    votes = get_latest_votes()

    mark_everything_as_processed()

    for message in tqdm(messages):
        send_message_to_steemit(message)

    for vote in tqdm(votes):
        send_vote_to_steemit(vote)

    # sleep(10)