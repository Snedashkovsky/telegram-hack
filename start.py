import click
from bot import bot
from steemit import synchronize as steemit
from rating import rate

def run_bot():
    print("Bot started...")
    bot.start()

def synchronize_steemit():
    print("Sync with steemit...")
    steemit.synchronize()

def synchronize_fluence():
    pass

def synchronize_ratings():
    print("Sync rating...")
    rate.rate()

PROCESSES = {
    "bot": run_bot,
    "steemit": synchronize_steemit,
    "rate": synchronize_ratings
}

@click.command()
@click.option('--process_name', help='Process', default="bot")
def process(process_name):
    PROCESSES[process_name]()

if (__name__ == "__main__"):
    process()