# import requests
from environs import Env
from google.cloud import dialogflow
from telegram import Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)


def implicit():
    from google.cloud import storage

    # If you don't specify credentials when constructing the client, the
    # client library will look for credentials in the environment.
    storage_client = storage.Client()

    # Make an authenticated API request
    buckets = list(storage_client.list_buckets())
    print(buckets)


def detect_intent_texts(project_id, session_id, text, language_code='RU'):
    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(
        text=text, language_code=language_code)

    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )

    return response.query_result.fulfillment_text


def create_and_start_bot(telegram_token):
    """Creates and launches a telegram bot."""
    updater = Updater(telegram_token)

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    updater.start_polling()

    updater.idle()


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    update.message.reply_text(f'Hi {user.first_name}!')


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    session_id = update.effective_user.id
    text = update.message.text

    update.message.reply_text(
        detect_intent_texts(
            'support-b10t-bot-16246',
            session_id,
            text)
    )


if __name__ == '__main__':
    env = Env()
    env.read_env()

    telegram_token = env.str('TELEGRAM_TOKEN')
    # google_application_credentials = env.str('GOOGLE_APPLICATION_CREDENTIALS')

    # telegram_chat_id = env.int('TELEGRAM_CHAT_ID', 0)
    # devman_token = env('DEVMAN_TOKEN', 'DEVMAN_TOKEN')

    create_and_start_bot(telegram_token)

    # user_reviews_url = 'https://dvmn.org/api/long_polling/'

    # headers = {
    #     'Authorization': f'Token {devman_token}',
    # }

    # params = {}

    # while True:
    #     try:
    #         response = requests.get(
    #             user_reviews_url,
    #             headers=headers,
    #             params=params
    #         )
    #     except requests.exceptions.ReadTimeout or requests.exceptions.ConnectionError:
    #         continue

    #     response.raise_for_status()

    #     reviews_result = response.json()

    #     print(reviews_result)

    #     if reviews_result['status'] == 'timeout':
    #         timestamp = int(reviews_result.get('timestamp_to_request'))
    #     else:
    #         timestamp = int(reviews_result.get('last_attempt_timestamp')) + 1

    #         for review in reviews_result.get('new_attempts'):
    #             review_status = 'Преподавателю всё понравилось, ' \
    #                 'можно переходить к следующему уроку.'

    #             if review.get('is_negative'):
    #                 review_status = 'К сожалению, в работе нашлись ошибки.'

    #             telegram_bot_message = f'У Вас проверили работу "{review.get("lesson_title")}".\n\n' \
    #                 f'{review_status}\n\n' \
    #                 f'Ссылка на урок: {review.get("lesson_url")}'

    #             telegram_bot.send_message(
    #                 chat_id=telegram_chat_id,
    #                 text=telegram_bot_message
    #             )

    #     params.update(timestamp=timestamp)
