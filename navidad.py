import urllib.request
import json
import time
import config
from slackclient import SlackClient

""" Automatismo tontorron para ver si te ha tocado algun numero de la loteria de navidad."""
""" Paco Brevers 2017 - 2018  - https://github.com/fbreversg/loteriaNavidadChecker """

# GLOBALES del script uuuuhhhhUUUUUUHHHHHH globales uuuuuuuhhhhhUUUUUUHHHHHHH.
resultados = []     # array de resultados
premiados = {}      # diccionario de premios para no repetir notificaciones salvo incrementos

# Sleeps para las comprobaciones (segundos).
ESPERA_COMPROBACION = 60
ESPERA_API = 1

# Numero solo para comprobar el estado del sorteo.
MAGIC_NUMBER = 42

# Endpoint cortesia de El Pais
ENDPOINT = 'http://api.elpais.com/ws/LoteriaNavidadPremiados?n='

# Literales de mensajes sobre el estado del sorteo.
ESTADO_CONCURSO = {0: 'Sorteo no ha empezado. Lo compruebo cada minuto.', 1: 'Resultados provisionales en carga. No pierdas la esperanza.', 2: 'Resultadosa a oido, es probable que tengas suerte.', 3: 'Resultados DEFINITIVOS. G0G0G0G0' }
LITERAL_ERROR_API = 'ERROR: El api me odia y no ha querido contestarme para el numero: {0}'
LITERAL_ERROR_API_RETRY = 'ERROR: Se ha reintentado pero el API me sigue odiando asi que GL y a esperar para el: {0}'
LITERAL_ERROR_API_MENSAJE = 'No se ha podido verificar el numero {}'
LITERAL_NO_TOCA = 'MOJON en {0} con {1}'
LITERAL_TOCA = 'PREMIO en {0} con {1} :tada:'
LITERAL_TOCA_MAS = 'INCREMENTO DE PREMIO en {0} de {1} a {2} CONGRATS!!! :tada: :tada: :tada: :tada:'


def calcula_premio (jugado, ganado_decimo):
    """ Funcion auxiliar para calcular el premio real en funcion de lo jugado """
    return ganado_decimo * jugado / 20


def verifica_numero(numero, jugado, retry=True):
    """Verifica si el numero ha sido premiado. retry permite una segunda consulta en caso de fallo."""

    # Cortesia para no reventarles el API
    time.sleep(ESPERA_API)

    # LLamada al API
    response = urllib.request.urlopen(ENDPOINT+str(numero))
    datos = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

    # Comprobacion de mensaje de vuelta del API.
    if datos['error'] == 0:
        # JSON OK
        return {'numero': datos['numero'], 'premio': calcula_premio(jugado, datos['premio'])}
    else:
        # Error de API
        print(LITERAL_ERROR_API.format(numero))
        # Se hace un reintento.
        if retry:
            print("Reintentandolo")
            verifica_numero(numero, jugado, retry=False)
        else:
            # Si despues del reintento no ha ido, se informa.
            print(LITERAL_ERROR_API_RETRY.format(numero))
            return {"numero": numero, "premio": -1}


def verifica_incremento(numero, premio):
    """ Verifica si un numero previamente premiado ha incrementado su premio.
    Devuelve True si hay incremento sobre un premio ya informado.
    False en caso contrario."""

    # Se comprueba si ya ha sido premiado previamente para no avisar de nuevo, pero antes se mira si se ha incrementado el premio.
    if numero in premiados.keys():
        if premiados[numero] < premio:
            # Premio mayor que el guardado.
            print(LITERAL_TOCA_MAS.format(numero, premiados[numero], premio))
            # Si hay integracion con slack se comunica.
            if sc:
                sc.api_call('chat.postMessage', channel=slack_user, text=LITERAL_TOCA_MAS.format(numero, premiados[numero], premio))
            # Se actualiza el nuevo premio.
            premiados[numero] = premio
        return True

    else:
        # Premio no informado. Se guarda
        premiados[numero] = premio
        return False


def main():

    # El bucle
    while True:

        # Comprobacion de estado del sorteo. No tiene sentido empezar a lanzar peticiones antes de tiempo.
        response = urllib.request.urlopen(ENDPOINT+str(MAGIC_NUMBER))
        estado = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

        # Imprime el estado del sorteo.
        status = estado['status']
        print(ESTADO_CONCURSO[status])

        # Si ha empezado ya.
        if status in (1, 2, 3, 4):

            # Comprobacion de numeros con reintento.
            for numero, jugado in numeros.items():
                resultados.append(verifica_numero(numero, jugado))

            # Comunicacion de resultados.
            for resultado in resultados:
                if resultado['premio'] > 0:
                    if not verifica_incremento(resultado['numero'], resultado['premio']):
                        print(LITERAL_TOCA.format(resultado['numero'], resultado['premio']))
                        # Si hay integracion con slack se comunica.
                        if sc:
                            sc.api_call('chat.postMessage', channel=slack_user, text=LITERAL_TOCA.format(resultado['numero'], resultado['premio']))
                elif resultado['premio'] < 0:
                    print(LITERAL_ERROR_API_MENSAJE.format(numero))
                else:
                    print(LITERAL_NO_TOCA.format(resultado['numero'], resultado['premio']))

            resultados.clear()
            print("Vuelvo a mirar en 1 minuto")

        # A esperar otra ronda.
        print("Esperando a que empiece.")
        time.sleep(ESPERA_COMPROBACION)


if __name__ == "__main__":

    # Numeros a comprobar
    numeros = config.numeros

    # Configuracion de slack
    if config.slack_token:
        sc = SlackClient(config.slack_token)
        slack_user = config.slack_user

    # A jugarrrrrr!!!!
    main()

