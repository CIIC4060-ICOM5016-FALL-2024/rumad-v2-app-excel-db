import psycopg2
from psycopg2 import pool
from config.dbconfig import pg_config

connection_pool = psycopg2.pool.SimpleConnectionPool(
    minconn=1,  # minimum number of connections in the pool
    maxconn=10,  # maximum connections
    user=pg_config["user"],
    password=pg_config["password"],
    host=pg_config["host"],
    database=pg_config["dbname"],
    port=pg_config["port"],
)


class DAO:

    def __init__(self):
        self.pool = connection_pool

    def create(self, query, values):
        """
        Connects to the PostgreSQL database and
        handles INSERT queries.
        :param query: the insert query format
        :param values: values to be inserted in list
        :return: True if success, False otherwise
        """
        with self.pool.getconn() as conn:  # get connection from pool
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)
                    tuple_id = cursor.fetchone()[0]
                    conn.commit()
                    return True, tuple_id
                except psycopg2.Error as e:
                    return False, e.pgcode, e.pgerror
                finally:
                    self.pool.putconn(conn)  # return connection to pool

    def read(self, query, values=None):
        """
        Connects to the PostgreSQL database and
        handles SELECT queries.
        :param query: query to be executed
        :param values: values to be formatted in
        :return: a list with a single tuple, many tuples, or None.
        False otherwise with error message
        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)
                    response = cursor.fetchall()
                    if not response:
                        return False, -1, "The request returned no response"
                    return response
                except psycopg2.Error as e:
                    return False, e.pgcode,  e.pgerror
                finally:
                    self.pool.putconn(conn)

    def update(self, query, values=None):
        """
        Connects to the PostgreSQL database and
        handles UPDATE queries.
        :param query: query to be executed
        :param values: values to be formatted in
        :return: True if success, False otherwise with error message
        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)

                    if cursor.rowcount == 0:
                        return False, -1, "Nothing to update"

                    conn.commit()
                    return True, cursor.statusmessage
                except psycopg2.Error as e:
                    return False, e.pgcode, e.pgerror
                finally:
                    self.pool.putconn(conn)

    def delete(self, query, values=None):
        """
        Connects to the PostgreSQL database and
        handles DELETE queries.
        :param values: values to be formatted in
        :param query: a query to be executed
        :return: True if success, False otherwise
        """
        with self.pool.getconn() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)

                    if cursor.rowcount == 0:
                        return False, -1, "Nothing to delete"

                    conn.commit()
                    return True, cursor.statusmessage

                except psycopg2.Error as e:
                    return False, e.pgcode, e.pgerror
                finally:
                    self.pool.putconn(conn)
