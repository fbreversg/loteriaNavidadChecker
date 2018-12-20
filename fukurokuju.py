import fukuControl
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
    if "añadir" in message:
        post_message(message='WARNING: En desarrollo.', channel=channel)
        if fukuControl.add_number(user, message):
            post_message(message='Numero añadido. Recuerda que puedes listar los que juegas en cualquier momento con "Listar"', channel=channel)
        else:
            post_message(
                message='Alguna se ha liado porque esto acaba de petar. ¿Seguro que no estas metiendo otra vez el mismo y sigues la sintaxis?"', channel=channel)
    elif "listar" in message:
        post_message(message='WARNING: En desarrollo.', channel=channel)
        numbers = fukuControl.list_numbers(user)
        if len(numbers) > 0:
            post_message(
                message='¡Suerte! Estos son los numeros añadidos y cantidad jugada:', channel=channel)
            for number in numbers:
                post_message(
                    message='Numero %s: %s euros' % number,  channel=channel)
        else:
            post_message(
                message='No me consta que hayas añadido nada =/', channel=channel)
    elif "borrar" in message:
        post_message(message='WARNING: En desarrollo.', channel=channel)
        if fukuControl.delete_number(user, message):
            post_message(
                message='Numero borrado.', channel=channel)
        else:
            post_message(
                message='Oops, la cosa es que no lo encuentro. ¿Estas seguro que lo estabas jugando?', channel=channel)
            numbers = fukuControl.list_numbers(user)
            if len(numbers) > 0:
                post_message(
                    message='Estos son los numeros añadidos y cantidad jugada:', channel=channel)
                for number in numbers:
                    post_message(
                        message='Numero %s: %s euros' % number, channel=channel)
            else:
                post_message(
                    message='No me consta que hayas añadido nada =/', channel=channel)
    elif "modificar" in message:
        post_message(message='WARNING: En desarrollo.', channel=channel)
        if fukuControl.update_amount(user, message):
            post_message(
                message='Cantidad jugada modificada.', channel=channel)
        else:
            post_message(
                message='Oops, la cosa es que no lo encuentro. ¿Estas seguro que lo estabas jugando?', channel=channel)
            numbers = fukuControl.list_numbers(user)
            if len(numbers) > 0:
                post_message(
                    message='Estos son los numeros añadidos y cantidad jugada:', channel=channel)
                for number in numbers:
                    post_message(
                        message='Numero %s: %s euros' % number, channel=channel)
            else:
                post_message(
                    message='No me consta que hayas añadido nada =/', channel=channel)

    elif "comprobar" in message:
        post_message(message='WARNING: En desarrollo.', channel=channel)
        prizes = fukuControl.check_prizes(user)
        if len(prizes) > 0:
            post_message(message=':tada: CONGRATS! Estos son tus numeros premiados: :tada:', channel=channel)
            for prize in prizes:
                post_message(message='Numero %s: / Jugado: %s euros / PREMIO: %s euros' % prize, channel=channel)
        else:
            post_message(message='De momento nada =/', channel=channel)
            post_message(message=':troll:', channel=channel)

    else:
        post_message(message='Dejame ayudarte, estos son los comandos que entiendo: ', channel=channel)
        post_message(message='añadir [numero] [cantidad] - Ej: añadir 12345 20', channel=channel)
        post_message(message='listar', channel=channel)
        post_message(message='modificar [numero] [cantidad] - Ej: modificar 12345 40', channel=channel)
        post_message(message='borrar [numero] - Ej: borrar 12345', channel=channel)
        post_message(message='comprobar', channel=channel)
        post_message(message='En el caso de que salga un numero premiado se supone que deberia avisarte, eso espero ;)', channel=channel)


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
