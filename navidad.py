import urllib.request
import json
import time

numeros = (33131,66859,67713,80472,46982,53243,11618)
resultados = []

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
