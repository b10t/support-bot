import logging
from textwrap import dedent

from environs import Env
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from google_df_api import detect_intent_text

logger = logging.getLogger('support-bot')


class BotLogsHandler(logging.Handler):
    def __init__(self, telegram_bot, telegram_chat_id) -> None:
        super().__init__()

        self.telegram_chat_id = telegram_chat_id
        self.telegram_bot = telegram_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.telegram_bot.send_message(
            chat_id=self.telegram_chat_id,
            text=dedent(log_entry)
        )


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg='Exception while handling an update:',
        exc_info=context.error
    )


def create_and_start_bot(telegram_token, telegram_chat_id):
    """Creates and launches a telegram bot."""
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, process_message))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    return dispatcher.bot


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Добро пожаловать в службу поддержки, {user.first_name}!')


def process_message(update: Update, context: CallbackContext) -> None:
    """Processes a message from the user."""
    session_id = update.effective_user.id
    message_text = update.message.text

    google_project_id = env.str('GOOGLE_PROJECT_ID')

    _, message_text = detect_intent_text(
        google_project_id,
        session_id,
        message_text
    )

    update.message.reply_text(message_text)


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING,
    )

    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')
    telegram_chat_id = env.int('TELEGRAM_CHAT_ID')

    telegram_bot = create_and_start_bot(telegram_token, telegram_chat_id)

    bot_logs_handler = BotLogsHandler(telegram_bot, telegram_chat_id)
    logger.addHandler(bot_logs_handler)
