import logging
import random

import vk_api
from environs import Env
from google.cloud import dialogflow
from vk_api.exceptions import ApiError
from vk_api.longpoll import VkEventType, VkLongPoll

logger = logging.getLogger('support-bot')


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


def process_message(event, vk_api, google_project_id):
    """Processes a message from the user."""
    session_id = event.user_id
    message_text = event.text

    message_text = detect_intent_text(
        google_project_id,
        session_id,
        message_text
    )

    vk_api.messages.send(
        user_id=session_id,
        message=message_text,
        random_id=random.randint(1, 1000)
    )


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING,
    )

    env = Env()
    env.read_env()

    google_project_id = env.str('GOOGLE_PROJECT_ID')
    vk_group_token = env.str('VK_GROUP_TOKEN')

    vk_session = vk_api.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()

    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            try:
                process_message(event, vk_api, google_project_id)
            except ApiError as api_error:
                error_code = api_error.error.get('error_code')
                error_msg = api_error.error.get('error_msg')

                logger.error(
                    f'[{error_code}]: {error_msg}'
                )
