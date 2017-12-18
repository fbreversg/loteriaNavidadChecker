# loteriaNavidadChecker

Script sencillo y rapido para verificar la loteria de navidad

Python 3.X

* pip install requirements.txt
* Editar config.py con los numeros que se juegan y opcionalmente un token de prueba de slack y tu usuario.

Para la integracion con slack:
* Obtener un token de prueba: https://api.slack.com/custom-integrations/legacy-tokens
* Lanzar el script con el parametro: SLACK_BOT_TOKEN="TOKEN_DE_TEST" python myapp.py

# Gracias a:

* ElPais.com por publicar su API de consulta.
* Jesus Esteban por su sugerencia de dar avisos.
* Alejandro Franco por pensar en los premios incrementales.
