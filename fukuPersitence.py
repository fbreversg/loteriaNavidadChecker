import logging
import mysql.connector

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# QUERIES
CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS FUKU_TABLE (
                            slack_id VARCHAR(12) NOT NULL ,
                            lucky_number integer NOT NULL ,
                            amount integer NOT NULL,
                            prize integer,
                            PRIMARY KEY(slack_id, lucky_number)
                            ); """

INSERT_NUMBER_QUERY = """INSERT INTO FUKU_TABLE(slack_id, lucky_number, amount, prize) 
                        VALUES (%s,%s,%s,%s)"""

SELECT_NUMBER_QUERY = """SELECT lucky_number, amount FROM FUKU_TABLE WHERE slack_id=%s"""

DELETE_NUMBER_QUERY = """DELETE FROM FUKU_TABLE WHERE slack_id=%s AND lucky_number=%s"""

UPDATE_AMOUNT_QUERY = """UPDATE FUKU_TABLE SET amount=%s WHERE slack_id=%s AND lucky_number=%s"""

CHECK_PRIZES_QUERY = """SELECT lucky_number, amount, prize FROM FUKU_TABLE WHERE slack_id=%s AND prize<>0"""


def create_connection(user, password, host, database):
    """ Conexion a BD."""
    try:
        conn = mysql.connector.connect(user=user, password=password, host=host, database=database)
    except mysql.connector.Error as e:
        logger.error(e)

    return conn


def create_table(conn):
    """ Creacion de tabla """
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
        cur.close()
    except mysql.connector.Error as e:
        logger.error(e)


def insert_number(conn, number):
    """ Insert de numeros """
    try:
        cur = conn.cursor()
        logger.debug('INSERT - "%s"', number)
        cur.execute(INSERT_NUMBER_QUERY, number)
        conn.commit()
        cur.close()
        return True
    except mysql.connector.Error as e:
        logger.error(e)
        logger.error('INSERT - "%s"', number)
        return False


def select_numbers(conn, slack_id):
    """ Listado de numeros asociados a usuario """
    try:
        cur = conn.cursor()
        logger.debug('SELECT - "%s"', slack_id)
        cur.execute(SELECT_NUMBER_QUERY, (slack_id,))
        rows = cur.fetchall()
        cur.close()
        return rows

    except mysql.connector.Error as e:
        logger.error(e)
        return ()


def delete_number(conn, slack_id, lucky_number):
    """ Borrado de numero """
    try:
        cur = conn.cursor()
        logger.debug('DELETE - %s / %s', slack_id, lucky_number)
        cur.execute(DELETE_NUMBER_QUERY, (slack_id, lucky_number))
        cur.close()
        return True
    except mysql.connector.Error as e:
        logger.error(e)
        return False


def update_amount(conn, slack_id, lucky_number, amount):
    """ Modificacion de dinero jugado a un numero """
    try:
        cur = conn.cursor()
        logger.debug('UPDATE - %s / %s / %s', slack_id, lucky_number, amount)
        cur.execute(UPDATE_AMOUNT_QUERY, (amount, slack_id, lucky_number))
        cur.close()
        return True
    except mysql.connector.Error as e:
        logger.error(e)
        return False


def check_prizes(conn, slack_id):
    """ Comprobacion de numeros premiados """
    try:
        cur = conn.cursor()
        logger.debug("CHECK - %s", slack_id)
        cur.execute(CHECK_PRIZES_QUERY, (slack_id,))
        rows = cur.fetchall()
        cur.close()
        return rows
    except mysql.connector.Error as e:
        logger.error(e)
        return 0
