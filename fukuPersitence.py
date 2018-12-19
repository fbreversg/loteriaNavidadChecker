import logging
import sqlite3
from sqlite3 import Error

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# QUERIES
CREATE_TABLE_QUERY = """CREATE TABLE IF NOT EXISTS FUKU_TABLE (
                            slack_id TEXT NOT NULL ,
                            lucky_number integer NOT NULL ,
                            amount integer NOT NULL,
                            prize integer,
                            PRIMARY KEY(slack_id, lucky_number)
                            ); """

INSERT_NUMBER_QUERY = """INSERT INTO FUKU_TABLE(slack_id, lucky_number, amount, prize) 
                        VALUES (?,?,?,?)"""

SELECT_NUMBER_QUERY = """SELECT lucky_number, amount FROM FUKU_TABLE WHERE slack_id=?"""

DELETE_NUMBER_QUERY = """DELETE FROM FUKU_TABLE WHERE slack_id=? AND lucky_number=?"""

UPDATE_AMOUNT_QUERY = """UPDATE FUKU_TABLE SET amount=? WHERE slack_id=? AND lucky_number=?"""


def create_connection(db_file):
    """ Conexion a BD. Si no existe la crea. """
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        logger.error(e)

    return conn


def create_table(conn):
    """ Creacion de tabla """
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_QUERY)
    except Error as e:
        logger.error(e)
    finally:
        if cur:
            cur.close()


def insert_number(conn, number):
    """ Insert de numeros """
    try:
        cur = conn.cursor()
        logger.debug('INSERT - "%s"', number)
        cur.execute(INSERT_NUMBER_QUERY, number)

    except Error as e:
        logger.error(e)
        logger.error('INSERT - "%s"', number)

    finally:
        if cur:
            cur.close()

    return cur.lastrowid


def select_numbers(conn, slack_id):
    """ Listado de numeros asociados a usuario """
    try:
        cur = conn.cursor()
        logger.debug('SELECT - "%s"', slack_id)
        cur.execute(SELECT_NUMBER_QUERY, (slack_id,))
        rows = cur.fetchall()

    except Error as e:
        logger.error(e)

    finally:
        if cur:
            cur.close()

    return rows


def delete_number(conn, slack_id, lucky_number):
    """ Borrado de numero """
    try:
        cur = conn.cursor()
        print (lucky_number)
        logger.debug('DELETE - %s / %s', slack_id, lucky_number)
        cur.execute(DELETE_NUMBER_QUERY, (slack_id, lucky_number))
        cur.close()
        return True
    except Error as e:
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
    except Error as e:
        logger.error(e)
        return False


def main():

    db_conn = create_connection("fukurokuju.db")
    with db_conn:
        create_table(db_conn)
        numero1 = ("AAAAAAA", 12345, 20, 0)
        numero2 = ("AAAAAAA", 54321, 20, 0)
        insert_number(db_conn, numero1)
        insert_number(db_conn, numero2)
        insert_number(db_conn, numero2)
        numbers = select_numbers(db_conn, "AAAAAAA")
        for number in numbers:
            print ("PRIMERA" + str(number))
        delete_number(db_conn, "AAAAAAA", 12345)
        delete_number(db_conn, "AAAAAAA", 54321)
        numbers = select_numbers(db_conn, "AAAAAAA")
        for number in numbers:
            print("SEGUNDA " + str(number))


if __name__ == '__main__':
    main()
