from commands.command import Command

class WelcomeCommand(Command):
    def run(self, message):
        self.bot.reply_to(message, "Just send a message with hashtag to save it")