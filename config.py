import os

config = {
    "BOT_TOKEN": os.environ["BOT_TOKEN"],
    "MONGO_HOST": "localhost",
    "MONGO_DATABASE": "telegram_hack",
    "MAPS_API_KEY": os.environ["MAPS_API_KEY"],
    "STEEMIT_KEY": os.environ["STEEMIT_KEY"],
    "STEEMIT_ACCOUNT": 'cyberdrop',

    "TEST_STEEMIT_PARENT": "test-post-for-telebot-decentralized-db",
    "TEST_MONGO_COLLECTION": "collection_test"
}