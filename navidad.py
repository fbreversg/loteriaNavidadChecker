import urllib.request
import json
import time

""" Automatismo tontorron para ver si te ha tocado algun numero de la loteria de navidad."""
""" Paco Brevers """

# Numeros a comprobar
numeros = (1, 2, 3, 4, 5)

magic_number = 42   # numero solo para comprobar el estado del sorteo.
resultados = []     # array de resultados
premiado = {}       # TODO: diccionario de premiados para "cachear" llamadas

# Literales de mensajes sobre el estado del sorteo.
estadoConcurso = {0: 'Sorteo no ha empezado. Lo compruebo cada minuto.', 1: 'Resultados provisionales en carga. No pierdas la esperanza.', 2: 'Resultadosa a oido, es probable que tengas suerte.', 3: 'Resultados DEFINITIVOS. G0G0G0G0' }
LITERAL_ERROR_API = 'ERROR: El api me odia y no ha querido contestarme para el numero: {0}'
LITERAL_ERROR_API_RETRY = 'ERROR: Se ha reintentado pero el API me sigue odiando asi que GL y a esperar para el: {0}'
LITERAL_ERROR_API_MENSAJE = 'No se ha podido verificar el numero {}'
LITERAL_NO_TOCA = 'MOJON en {0} con {1}'
LITERAL_TOCA = 'PREMIO en {0} con {1}'

# Endpoint cortesia de El Pais
ENDPOINT = 'http://api.elpais.com/ws/LoteriaNavidadPremiados?n='


def verifica_numero(numero, retry=True):
    """Verifica si el numero ha sido premiado. retry permite una segunda consulta en caso de fallo."""

    # Cortesia para no reventarles el API
    time.sleep(1)

    response = urllib.request.urlopen(ENDPOINT+str(numero))
    datos = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

    if datos['error'] == 0:
        return {"numero": datos['numero'], "premio": datos['premio']}
    else:
        print(LITERAL_ERROR_API.format(numero))
        if retry:
            print("Reintentandolo")
            verifica_numero(numero, retry=False)
        else:
            print(LITERAL_ERROR_API_RETRY.format(numero))
            return {"numero": numero, "premio": -1}


def main():
    while True:

        response = urllib.request.urlopen(ENDPOINT+str(magic_number))
        estado = json.loads(response.read().decode('utf8').replace('busqueda=', ''))

        status = estado['status']
        print(estadoConcurso[status])

        if status in (1, 2, 3, 4):

            for numero in numeros:
                resultados.append(verifica_numero(numero))

            for resultado in resultados:
                if resultado['premio'] > 0:
                    print(LITERAL_TOCA.format(resultado['numero'], resultado['premio']))
                elif resultado['premio'] < 0:
                    print(LITERAL_ERROR_API_MENSAJE.format(numero))
                else:
                    print(LITERAL_NO_TOCA.format(resultado['numero'], resultado['premio']))

            print("A ver si a la siguiente")

        # A esperar otra ronda.
        time.sleep(60)


if __name__ == "__main__":
    main()

