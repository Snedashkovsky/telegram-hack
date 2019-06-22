from commands.command import Command
from datetime import datetime

class SaveCommand(Command):
    def _extract_text(self, text):
        return text[len("/save") + 1:]

    def _save_to_collection(self, message):
        collection = self._get_collection(message)
        author = self._get_author(message)
        message_id = self._get_message_id(message)
        self.database[collection].save({
            "_id": message_id,
            "author": author,
            "text": self._extract_text(message.text),
            "created_at": datetime.now()
        })

    def _send_message(self, message):
        self.bot.reply_to(message, "Your message was saved")

    def run(self, message):
        self._save_to_collection(message)
        self._send_message(message)