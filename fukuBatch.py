""" Tarea que comprueba periodicamente los numeros premiados y actualiza DB """

import fukuControl
import json
import logging
import time
import urllib.request


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Endpoint cortesia de El Pais
ENDPOINT = 'http://api.elpais.com/ws/LoteriaNavidadPremiados?n='

# Sleeps para las comprobaciones (segundos).
ESPERA_COMPROBACION = 60
ESPERA_API = 1

# Numero solo para comprobar el estado del sorteo.
MAGIC_NUMBER = 42

# Literales de mensajes sobre el estado del sorteo.
ESTADO_CONCURSO = {0: 'Sorteo no ha empezado. Lo compruebo cada minuto.', 1: 'Resultados provisionales en carga. No pierdas la esperanza.', 2: 'Resultadosa a oido, es probable que tengas suerte.', 3: 'Resultados DEFINITIVOS. G0G0G0G0' }
LITERAL_ERROR_API_MENSAJE = 'No se ha podido verificar el numero {}'
LITERAL_ERROR_API_NO_DISPONIBLE = 'API no disponible en este momento.'
LITERAL_ERROR_API = 'ERROR: El api me odia y no ha querido contestarme para el numero: {0}'
LITERAL_ERROR_API_RETRY = 'ERROR: Se ha reintentado pero el API me sigue odiando asi que GL y a esperar para el: {0}'


def comprobar_estado_sorteo():

    #TODO: Eliminar
    return True

    # Comprobacion de estado del sorteo. No tiene sentido empezar a lanzar peticiones antes de tiempo.
    response = urllib.request.urlopen(ENDPOINT+str(MAGIC_NUMBER))
    estado = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

    if estado['error'] == 1:
        logger.error(LITERAL_ERROR_API_NO_DISPONIBLE)
        return False
    else:
        # Imprime el estado del sorteo.
        status = estado['status']
        logging.info(ESTADO_CONCURSO[status])

        # Si ha empezado ya...
        return status in (1, 2, 3, 4)


def calcula_premio (jugado, ganado_decimo):
    """ Funcion auxiliar para calcular el premio real en funcion de lo jugado """
    return ganado_decimo * jugado / 20


def verifica_numero(numero, retry=True):
    """Verifica si el numero ha sido premiado. retry permite una segunda consulta en caso de fallo."""

    #TODO: Eliminar
    if numero == 20000:
        return 30
    else:
        return 20

    # Cortesia para no reventarles el API
    time.sleep(ESPERA_API)

    # LLamada al API
    response = urllib.request.urlopen(ENDPOINT+str(numero))
    print(ENDPOINT+str(numero))
    datos = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

    # Comprobacion de mensaje de vuelta del API.
    if datos['error'] == 0:
        return datos['premio']
    else:
        # Error de API
        logger.error(LITERAL_ERROR_API.format(numero))
        # Se hace un reintento.
        if retry:
            logger.info("Reintentandolo")
            verifica_numero(numero, retry=False)
        else:
            # Si despues del reintento no ha ido, se informa.
            logger.error(LITERAL_ERROR_API_RETRY.format(numero))
            return -1


def run_batch():
    """ Tarea de ejecucion del batch """

    logger.info("Arranque del batch.")
    if comprobar_estado_sorteo():
        numbers = fukuControl.list_all_numbers()
        for number in numbers:
            prize = verifica_numero(number)
            if prize > 0:
                fukuControl.add_update_prize(number, prize)

            # Recuperacion de premiados para comunicar
            prized = fukuControl.list_prized()
            print(prized)

            # Actualizacion de importes premiados
            fukuControl.update_prizes(number, prize)


if __name__ == '__main__':
    run_batch()

