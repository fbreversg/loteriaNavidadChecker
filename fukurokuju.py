import logging
import os
import slackclient
import time

FUKU_SLACK_TOKEN = os.environ.get('FUKU_SLACK_TOKEN')
FUKU_SLACK_NAME = os.environ.get('FUKU_SLACK_NAME')
FUKU_SLACK_ID = os.environ.get('FUKU_SLACK_ID')

# Frecuencia de consulta al stream de slack.
SOCKET_DELAY = 1

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable slack client
fuku_slack_client = slackclient.SlackClient(FUKU_SLACK_TOKEN)


def is_for_me(event):
    """ Auxiliar para saber si el mensaje es para el bot por privado o canal. """
    event_type = event.get('type')
    if event_type and event_type == 'message' and not (event.get('user') == FUKU_SLACK_ID):
        if is_private(event):
            return True
        text = event.get('text')
        if get_mention(FUKU_SLACK_ID) in text.strip().split():
            return True


def handle_message(message, user, channel):
    """ Dispatcher de comandos. """
    if "Añadir" in message:
        post_message(message='Añadir command: Estamos en ello.', channel=channel)
    elif "Listar" in message:
        post_message(message='Listar command: Estamos en ello.', channel=channel)
    elif "Borrar" in message:
        post_message(message='Borrar command: Estamos en ello.', channel=channel)
    else:
        post_message(message='Dejame ayudarte, estos son los comandos que entiendo: Añadir, Listar, Borrar',
                     channel=channel)


def post_message(message, channel):
    """ Encapsulacion de envio de mensajes """
    fuku_slack_client.api_call('chat.postMessage', channel=channel, text=message, as_user=True)


def is_private(event):
    """Chechenada al canto para saber si es privado."""
    return event.get('channel').startswith('D')


def get_mention(user):
    """ Formateo para las menciones. """
    return '<@{user}>'.format(user=user)


def run():
    if fuku_slack_client.rtm_connect():
        logger.info('Fukurokuju al aparato. ¡Buena suerte!')
        while True:
            event_list = fuku_slack_client.rtm_read()
            if len(event_list) > 0:
                for event in event_list:
                    logger.debug(event)
                    if is_for_me(event):
                        handle_message(message=event.get('text'), user=event.get('user'), channel=event.get('channel'))
            time.sleep(SOCKET_DELAY)
    else:
        logger.error("Fallo en la conexion con SLACK! WE'RE FUCKED!")


if __name__ == '__main__':
    run()