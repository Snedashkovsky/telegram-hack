from commands.command import Command

class SaveCommand(Command):
    def _extract_collection(self, message):
        return message.text.split("\n")[0].strip() + "_messages"

    def _save_to_collection(self, collection, message):
        self.database[collection].save({
            "text": message.text
        })

    def _send_message(self, collection, message):
        self.bot.reply_to(message, "Your message was sended to a collection {}".format(collection))

    def run(self, message):
        collection = self._extract_collection(message)
        self._save_to_collection(collection, message)
        self._send_message(collection, message)