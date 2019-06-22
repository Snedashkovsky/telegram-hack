from commands.command import Command
from pymongo import MongoClient
from config import config

class ShowCommand():
    def _extract_number(self, message):
        return min(int(message.text.split(" ")[1]), 0) 

    def _get_messages(self, number):
        return self.

    def run(self, message):
        number = self._extract_collection(message)
        messages = self._get_messages(number)
        self._send_messages(message, messages)