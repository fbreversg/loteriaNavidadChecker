""" Logica del bot."""
import fukuPersistence
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

FUKU_MYSQL_USER = os.environ.get('FUKU_MYSQL_USER')
FUKU_MYSQL_PASS = os.environ.get('FUKU_MYSQL_PASS')
FUKU_MYSQL_HOST = os.environ.get('FUKU_MYSQL_HOST')
FUKU_MYSQL_DB = os.environ.get('FUKU_MYSQL_DB')

db_conn = fukuPersistence.create_connection(FUKU_MYSQL_USER, FUKU_MYSQL_PASS, FUKU_MYSQL_HOST, FUKU_MYSQL_DB)


def add_number(user, message):
    params = __parse_add_update__(message)
    if params:
        logger.debug("Add / Update %s: %s / %s euros", user, params[0], params[1])
        return fukuPersistence.insert_number(db_conn, (user, params[0], params[1], 0))
    else:
        return False


def add_update_prize(number, prize):
    logger.debug("Add / update prize: %s / %s", number, prize)
    # Para detectar "repremios" se intenta el insert y si no se hace update.
    fukuPersistence.insert_prize(db_conn, number, prize)


def update_prizes(number, prize):
    logger.debug("Update prizes: %s / %s", number, prize)
    fukuPersistence.update_prizes(db_conn, number, prize)


def delete_number(user, message):
        params = __parse_delete__(message)
        if params:
            logger.debug("Delete %s: %s", user, params[0])
            return fukuPersistence.delete_number(db_conn, user, params[0])
        else:
            return False


def list_numbers(user):
    logger.debug("List %s", user)
    return fukuPersistence.select_numbers(db_conn, user)


def list_all_numbers():
    logger.debug("List all numbers")
    return fukuPersistence.select_all_numbers(db_conn)


def list_prized():
    logger.debug("List prized")
    return fukuPersistence.select_prized(db_conn)


def update_amount(user, message):
    params = __parse_add_update__(message)
    if params:
        logger.debug("Update %s: %s / %s euros", user, params[0], params[1])
        return fukuPersistence.update_amount(db_conn, user, params[0], params[1])
    else:
        return False


def check_prizes(user):
    logger.debug("CHECK %s", user)
    numbers = fukuPersistence.check_prizes(db_conn, user)
    if len(numbers) > 0:
        prizes = []
        for number in numbers:
            prizes.append((number[0], number[1], number[1]*number[2]))
        return prizes
    else:
        return ()


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
            return params[1],

    return None
