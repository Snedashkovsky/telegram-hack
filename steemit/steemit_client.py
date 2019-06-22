import steembase
from steem import Steem
import random
import string
from config import config

class SteemitClient():
    def __init__(self,account,private_key):
        self.account_name = account
        self.connection = Steem(keys=[private_key])

    # TODO not working
    def send_post(self, author, title, body):
        assert False
        self.connection.commit.post(title,msg_body,self.account_name)
    
    def send_low_level_post(self, author, title, body, parent_link):
        self.connection.commit.post(title, body, self.account_name, reply_identifier=f'{self.account_name}/{parent_link}')
    
    # TODO return only comments by author
    def get_posts(self, index_from, posts_limit):
        all_history = self.connection.get_account_history(self.account_name, index_from, posts_limit)
        return [i for i in all_history if i[1]['op'][0] == 'comment']


if (__name__ == "__main__"): 
    key = config["STEEMIT_KEY"]
    account_name = config["STEEMIT_ACCOUNT"]
    test = SteemitClient(account_name, key)
    answer = test.get_posts(-1, 1)