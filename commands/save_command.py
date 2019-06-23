from commands.command import Command
from datetime import datetime
import requests
from config import config

MAPS_API_PATH = 'https://api.opencagedata.com/geocode/v1/json'

def get_location(text):
    response = requests.get(MAPS_API_PATH, params={
        "q": text,
        "key": config["MAPS_API_KEY"]
    })
    response_json = response.json()
    location = None
    if response_json["results"]:
        location = response_json['results'][0]['geometry']
    return location

class SaveCommand(Command):
    def __init__(self, bot):
        super().__init__(bot)

    def _get_text(self, text):
        return text[len("/save") + 1:]

    def _get_location(self, text):
        return get_location(text)

    def _save_to_collection(self, message):
        author = self._get_author(message)
        message_id = self._get_message_id(message)
        address = self._get_text(message.text)
        message_dict = {
            "_id": message_id,
            "author": author,
            "address": address,
            "location": self._get_location(address),
            "created_at": datetime.now()
        }

        self._save_to_blockchain(message_dict)
        self._save_to_mongo(message, message_dict)

    def _send_message(self, message):
        self.bot.reply_to(message, "Thanks! Your address was saved")

    def run(self, message):
        self._save_to_collection(message)
        self._send_message(message)