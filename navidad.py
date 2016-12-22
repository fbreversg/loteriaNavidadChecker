import urllib.request
import json
import time

numeros = (1,2,3,4,5)
resultados = []

while True:

    for numero in numeros:
        response = urllib.request.urlopen('http://api.elpais.com/ws/LoteriaNavidadPremiados?n='+str(numero))
        datos = json.loads(response.read().decode('utf8').replace('busqueda=', ''))
        if datos['error'] == 0:
            resultados.append(datos)
        else:
            while datos['error'] != 0:
                response = urllib.request.urlopen('http://api.elpais.com/ws/LoteriaNavidadPremiados?n='+str(numero))
                datos = json.loads(response.read().decode('utf8').replace('busqueda=', ''))
                if datos['error'] == 0:
                    resultados.append(datos)
                time.sleep(0.5)

    for resultado in resultados:
        if resultado['premio'] > 0:
            print('PREMIO en %s con %s' % (resultado['numero'], resultado['premio']))
        else:
            print('MOJON en %s con %s' % (resultado['numero'], resultado['premio']))

    print("A ver si a la siguiente")
    time.sleep(60)