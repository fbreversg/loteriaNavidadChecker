""" Logica del bot."""
import fukuPersitence
import logging
import os

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

FUKU_MYSQL_USER = os.environ.get('FUKU_MYSQL_USER')
FUKU_MYSQL_PASS = os.environ.get('FUKU_MYSQL_PASS')
FUKU_MYSQL_HOST = os.environ.get('FUKU_MYSQL_HOST')
FUKU_MYSQL_DB = os.environ.get('FUKU_MYSQL_DB')

db_conn = fukuPersitence.create_connection(FUKU_MYSQL_USER, FUKU_MYSQL_PASS, FUKU_MYSQL_HOST, FUKU_MYSQL_DB)


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


def check_prizes(user):
    logger.debug("CHECK %s", user)
    numbers = fukuPersitence.check_prizes(db_conn, user)
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
            print ("PARSE", params[1])
            return params[1],

    return None
