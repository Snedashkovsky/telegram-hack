from commands.command import Command
from datetime import datetime


class VoteCommand(Command):
    def __init__(self, bot, vote=1):
        super().__init__(bot)
        self.vote = vote

    def _validate_vote(self, message):
        reply_to_message = message.reply_to_message
        return reply_to_message is not None

    def _get_author_from_bot_message(self, message):
        url = message.text.split("\n")[-1]
        user = url.split("aid=")[-1]
        return user

    def _get_vote_collection(self, message):
        return "{}_{}".format(self._get_collection(message), "votes")

    def _save_to_collection(self, message):
        collection = self._get_vote_collection(message)
        votee = self._get_author_from_bot_message(message.reply_to_message)
        voter = self._get_author(message)
        message_id = self._get_message_id(message)

        self.database[collection].save({
            "_id": message_id,
            "voter": voter,
            "votee": votee,
            "created_at": datetime.now(),
            "vote": self.vote
        })

    def _send_message(self, message):
        self.bot.reply_to(message, "Thanks! Your vote was saved")

    def run(self, message):
        if self._validate_vote(message):
            self._save_to_collection(message)
            self._send_message(message)
