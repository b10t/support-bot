import json
import logging

from environs import Env
from google.cloud import dialogflow
from google.cloud.exceptions import BadRequest


logger = logging.getLogger('support-bot')


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(
            text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name, training_phrases=training_phrases, messages=[
            message]
    )

    response = intents_client.create_intent(
        request={"parent": parent, "intent": intent}
    )

    print("Intent created: {}".format(response))


if __name__ == '__main__':
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.WARNING,
    )

    env = Env()
    env.read_env()

    google_project_id = env.str('GOOGLE_PROJECT_ID')

    with open('questions.json', 'r') as questions_file:
        training_phrases = json.load(questions_file)

    for phrase in training_phrases:
        training_intent = training_phrases.get(phrase)

        questions = training_intent.get('questions')
        answer = training_intent.get('answer')

        try:
            create_intent(
                google_project_id,
                phrase,
                questions,
                [answer]
            )
        except BadRequest as err:
            logger.error(err.message)
