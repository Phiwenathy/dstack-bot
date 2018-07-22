#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import operator
import os
from datetime import datetime

import dotenv
import psutil
from invoke import run
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

dotenv.load_dotenv(dotenv.find_dotenv())

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger('dstack_cubed')

token = os.getenv('TELEGRAM_BOT_TOKEN')
only_me = Filters.user(username=os.getenv('TELEGRAM_BOT_ADMIN'))


# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(bot, update):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def invoke(bot, update):
    """Run message as invoke task"""
    result = run(update.message.text, hide=True, warn=True, pty=False)
    update.message.reply_markdown(f'```bash\n{result.stdout or "No output."}\n```')


def error(bot, update, error_name):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error_name)


def stats(bot, update):
    memory = psutil.virtual_memory()
    disk = psutil.disk_usage('/')
    boot_time = datetime.fromtimestamp(psutil.boot_time())
    now = datetime.now()
    time_diff = "Online for: %.1f Hours" % (((now - boot_time).total_seconds()) / 3600)
    memory_total = "Total memory: %.2f GB " % (memory.total / 1000000000)
    memory_available = "Available memory: %.2f GB" % (memory.available / 1000000000)
    memory_used_percentage = "Used memory: " + str(memory.percent) + " %"
    disk_used = "Disk used: " + str(disk.percent) + " %"
    pids = psutil.pids()
    pids_reply = ''
    processes = {}
    for pid in pids:
        p = psutil.Process(pid)
        try:
            process_memory_percentage = p.memory_percent()
            if process_memory_percentage > 0.5:
                if p.name() in processes:
                    processes[p.name()] += process_memory_percentage
                else:
                    processes[p.name()] = process_memory_percentage
        except (psutil.AccessDenied, psutil.ZombieProcess):
            pass
    sorted_processes = sorted(processes.items(), key=operator.itemgetter(1), reverse=True)
    for process in sorted_processes:
        pids_reply += process[0] + " " + ("%.2f" % process[1]) + " %\n"

    update.message.reply_markdown(
        '```bash\n'
        f'{time_diff}\n'
        f'{memory_total}\n'
        f'{memory_available}\n'
        f'{memory_used_percentage}\n'
        f'{disk_used}\n'
        f'{pids_reply}\n'
        '```'
    )


def main():
    """Start the bot."""
    # Create the EventHandler and pass it your bot's token.
    updater = Updater(token)
    # Get the dispatcher to register handlers
    dp = updater.dispatcher
    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start, filters=only_me))
    dp.add_handler(CommandHandler("stats", stats, filters=only_me))
    # on non-command i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & only_me, invoke))
    # log all errors
    dp.add_error_handler(error)
    # Start the Bot
    updater.start_polling()
    logger.info('Bot started')
    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()
