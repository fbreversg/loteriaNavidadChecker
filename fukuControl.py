""" Logica del bot."""
import fukuPersitence
import logging

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# DB sqlite
DB = "fukurokuju.db"
# Conexion a BD.
db_conn = fukuPersitence.create_connection(DB)


def add_number(user, message):
    params = __parse_add_update__(message)
    if params:
        logger.debug("Add / Update %s: %s / %s euros", user, params[0], params[1])
        return fukuPersitence.insert_number(db_conn, (user, params[0], params[1], 0))
    else:
        return False


def delete_number(user, message):
        params = __parse_delete__(message)
        if params:
            logger.debug("Delete %s: %s", user, params[0])
            print("DELETE", params[0])
            return fukuPersitence.delete_number(db_conn, user, params[0])
        else:
            return False


def list_numbers(user):
    logger.debug("List %s", user)
    numbers = fukuPersitence.select_numbers(db_conn, user)
    return numbers


def update_amount(user, message):
    params = __parse_add_update__(message)
    if params:
        logger.debug("Update %s: %s / %s euros", user, params[0], params[1])
        return fukuPersitence.update_amount(db_conn, user, params[0], params[1])
    else:
        return False


def __parse_add_update__(message):
    params = message.split()
    if len(params) == 3:
        if params[1].isnumeric() and params[2].isnumeric():
            return params[1], params[2]

    return None


def __parse_delete__(message):
    params = message.split()
    if len(params) == 2:
        if params[1].isnumeric():
            print ("PARSE", params[1])
            return params[1],

    return None
