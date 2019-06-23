import steembase
from steem import Steem
import random
import string
# from config import config

# TODO remove from this place
config = {
    "BOT_TOKEN": "765705629:AAH9YsCDdYHWsEWiSlKWPFwFHOijynwOU5A", #os.environ["BOT_TOKEN"],
    "MONGO_HOST": "localhost",
    "MONGO_DATABASE": "telegram_hack",
    "MAPS_API_KEY": "0d28c99c928f4c1da4433bd10bf94838", #os.environ["GMAPS_API_KEY"]
    "STEEMIT_KEY": "5K5DA2kmJqLew5fDcwBaV44BKUGHiHCnefDzVFJvvQ6M9XNGnF2", #os.environ["GMAPS_API_KEY"]
    "STEEMIT_ACCOUNT": 'cyberdrop',

    "TEST_STEEMIT_PARENT": "test-post-for-telebot-decentralized-db",
    "TEST_MONGO_COLLECTION": "collection_test"
}

class SteemitClient():
    def __init__(self,account,private_key):
        self.account_name = account
        self.connection = Steem(keys=[private_key])

    # TODO not working
    def send_post(self, author, title, body):
        assert False
        self.connection.commit.post(title,msg_body,self.account_name)
    
    def send_low_level_post(self, author, title, body, parent_link):
        # TODO reply not working
        self.connection.commit.post(title, body, self.account_name, reply_identifier=f'{self.account_name}/{parent_link}')
    
    def get_posts(self,permlink_collection):
        votes = []
        msgs = []

        for i in self.connection.get_content_replies(self.account_name, permlink_collection):
            if i['author'] == self.account_name:
                permlink = i['permlink']
                parent_permlink = i['parent_permlink']
                body_row = i['body']
                msgs.append(body_row)
                
                for j in self.connection.get_content_replies(self.account_name, permlink):
                    if j['author'] == self.account_name:
                        permlink = j['permlink']
                        parent_permlink = j['parent_permlink']
                        body_row = j['body']
                        votes.append(body_row)

        return msgs, votes


if (__name__ == "__main__"): 
    key = config["STEEMIT_KEY"]
    account_name = config["STEEMIT_ACCOUNT"]
    test = SteemitClient(account_name, key)
    answer = test.get_posts(-1, 1)