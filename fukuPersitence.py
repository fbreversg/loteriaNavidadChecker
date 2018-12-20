import logging
import mysql.connector

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(__name__)

# QUERIES
CREATE_TABLE_FUKU_QUERY = """CREATE TABLE IF NOT EXISTS FUKU_TABLE (
                            slack_id VARCHAR(12) NOT NULL ,
                            lucky_number integer NOT NULL ,
                            amount integer NOT NULL,
                            prize integer,
                            PRIMARY KEY(slack_id, lucky_number)
                            ); """

CREATE_TABLE_FUKU_PRIZES_QUERY = """CREATE TABLE IF NOT EXISTS FUKU_PRIZES_TABLE (
                                lucky_number integer NOT NULL PRIMARY KEY,
                                prize integer
                                );"""

INSERT_NUMBER_QUERY = """INSERT INTO FUKU_TABLE(slack_id, lucky_number, amount, prize) 
                        VALUES (%s,%s,%s,%s)"""

INSERT_PRIZE_QUERY = """INSERT INTO FUKU_PRIZES_TABLE(lucky_number, prize) 
                        VALUES (%s,%s)"""

UPDATE_PRIZE_QUERY = """UPDATE FUKU_PRIZES_TABLE SET prize=%s WHERE lucky_number=%s"""

SELECT_NUMBER_QUERY = """SELECT lucky_number, amount FROM FUKU_TABLE WHERE slack_id=%s"""

SELECT_PRIZES_QUERY = """SELECT lucky_number, prize FROM FUKU_PRIZES_TABLE"""

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


def create_fuku_table(conn):
    """ Creacion de tabla de usuarios, numeros"""
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_FUKU_QUERY)
        cur.close()
    except mysql.connector.Error as e:
        logger.error(e)


def create_fuku_prizes_table(conn):
    """ Creacion de tabla para numeros / premios"""
    try:
        cur = conn.cursor()
        cur.execute(CREATE_TABLE_FUKU_PRIZES_QUERY)
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


def insert_prize(conn, number, prize):
    """ Insert de premios """
    try:
        cur = conn.cursor()
        logger.debug('INSERT PRIZE - "%s" / "%s"', number, prize)
        cur.execute(INSERT_PRIZE_QUERY, (number, prize))
        conn.commit()
        cur.close()
        return True

    except mysql.connector.Error as e:
        logger.error(e)
        logger.error('INSERT PRIZE - "%s" / "%s"', number, prize)
        return False


def update_prize(conn, number, prize):
    """ Update de premio """
    try:
        cur = conn.cursor()
        logger.debug('UPDATE PRIZE - "%s" / "%s"', number, prize)
        cur.execute(UPDATE_PRIZE_QUERY, (number, prize))
        conn.commit()
        cur.close()
        return True

    except mysql.connector.Error as e:
        logger.error(e)
        logger.error('UPDATE PRIZE - "%s" / "%s"', number, prize)
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


def select_prizes(conn):
    """ Listado de numeros premiados"""
    try:
        cur = conn.cursor()
        logger.debug('SELECT PRIZES')
        cur.execute(SELECT_PRIZES_QUERY)
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


if __name__ == "__main__":
    db_conn = create_connection("root", "root", "127.0.0.1", "fukurokuju")
    create_fuku_prizes_table(db_conn)
    select_prizes(db_conn)
    insert_prize(db_conn, 12345, 20)
    select_prizes(db_conn)
    insert_prize(db_conn, 12345, 20)
    update_prize(db_conn, 12345, 40)
    select_prizes(db_conn)
