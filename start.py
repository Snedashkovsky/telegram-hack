import click
from bot import bot
from blockchains import synchronize as blockchains
from rating import rate
from config import config

def run_bot():
    print("Bot started...")
    bot.start()

def synchronize_blockchain():
    print("Sync with {}...".format(config["BLOCKCHAIN_CLIENT"]))
    blockchains.synchronize()

def synchronize_ratings():
    print("Sync rating...")
    rate.rate()

PROCESSES = {
    "bot": run_bot,
    "blockchain": synchronize_blockchain,
    "rate": synchronize_ratings
}

@click.command()
@click.option('--process_name', help='Process', default="bot")
def process(process_name):
    PROCESSES[process_name]()

if (__name__ == "__main__"):
    process()