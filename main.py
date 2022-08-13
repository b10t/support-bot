import logging
from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def error_handler(update: object, context: CallbackContext) -> None:
    logger.error(
        msg='Exception while handling an update:',
        exc_info=context.error
    )


def detect_intent_text(project_id, session_id, text, language_code='RU'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={'session': session, 'query_input': query_input}
    )

    return response.query_result.fulfillment_text


def create_and_start_bot(telegram_token):
    """Creates and launches a telegram bot."""
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    dispatcher.add_error_handler(error_handler)

    updater.start_polling()

    updater.idle()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(
        f'Добро пожаловать в службу поддержки, {user.first_name}!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    session_id = update.effective_user.id
    message_text = update.message.text

    google_project_id = env.str('GOOGLE_PROJECT_ID')

    update.message.reply_text(
        detect_intent_text(
            google_project_id,
            session_id,
            message_text
        )
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')

    create_and_start_bot(telegram_token)
