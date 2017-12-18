# loteriaNavidadChecker

Script sencillo y rápido para verificar la lotería de navidad.

Python 3.x

* pip install requirements.txt
* Editar config.py con los números e importe que se juegan y opcionalmente un token de prueba de slack y tu usuario.
* python navidad.py

Para la integracion con slack:
* Obtener un token de prueba: https://api.slack.com/custom-integrations/legacy-tokens

# Últimas Features

* Integracion con slack (OPCIONAL). Ahora te avisará de si te toca por mensaje privado.
* Externalizada la parametrización de números jugados y se informa la cantidad jugada.
* Premio real en función del dinero jugado al número.


# Gracias a:

* ElPais.com por publicar su API de consulta.
* Jesus Esteban (https://github.com/txesus) por su sugerencia de dar avisos y mostrar el premio real en funcion de lo jugado.
* Alejandro Franco (https://github.com/afrasilv) por pensar en los premios incrementales.

# DISCLAIMER

Hecho para uso personal si no te funciona BUSCA EN GOOGLE! ;)
