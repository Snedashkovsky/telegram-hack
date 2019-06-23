from blockchains import synchronize as blockchains
from commands.command import Command

class SynchronizeCommand(Command):
    def run(self, message):
        try:
            blockchains.synchronize()
            self.bot.reply_to(message, "DB Synchronized!")
        except Exception as e:
            self.bot.reply_to(message, "There is an exception")
            raise e