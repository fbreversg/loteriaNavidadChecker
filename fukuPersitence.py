import logging
import sqlite3
from sqlite3 import Error

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
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
        c = conn.cursor()
        c.execute(CREATE_TABLE_QUERY)
    except Error as e:
        logger.error(e)


def insert_number(conn, number):
    """ Insert de numeros """
    cur = conn.cursor()
    cur.execute(INSERT_NUMBER_QUERY, number)
    return cur.lastrowid


def main():

    db_conn = create_connection("fukurokuju.db")
    if db_conn:
        create_table(db_conn)
        numero1 = ("AAAAAAA", 12345, 20, 0)
        numero2 = ("AAAAAAA", 54321, 20, 0)
        insert_number(db_conn, numero1)
        insert_number(db_conn, numero2)

    else:
        logger.error("No se ha podido conectar con la BD. WTF!")


if __name__ == '__main__':
    main()
