import psycopg
from psycopg_pool import ConnectionPool
from config.dbconfig import pg_config

url = ("dbname=%s password=%s host=%s port=%s user=%s" %
       (pg_config['dbname'],
        pg_config['password'],
        pg_config['host'],
        pg_config['port'],
        pg_config['user']))

pool = ConnectionPool(url)


class DAO:

    def __init__(self):
        self.pool = pool

    def create(self, query, values):
        """
        Connects to the PostgreSQL database and
        handles INSERT queries.
        :param query: the insert query format
        :param values: values to be inserted in list
        :return: True if success, False otherwise
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query, values)
                    return True
                except psycopg.Error:
                    return False

    def read(self, query):
        """
        Connects to the PostgreSQL database and
        handles SELECT queries.
        :param query: query to be executed
        :return: a list with a single tuple, many tuples, or None
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    return cursor.fetchall()
                except psycopg.Error:
                    return False

    def update(self, query):
        """
        Connects to the PostgreSQL database and
        handles UPDATE queries.
        :param query: query to be executed
        :return: True if success, False otherwise
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    return True
                except psycopg.Error:
                    return False

    def delete(self, query):
        """
        Connects to the PostgreSQL database and
        handles DELETE queries.
        :param query: query to be executed
        :return: True if success, False otherwise
        """
        with self.pool.connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(query)
                    return True
                except psycopg.Error:
                    return False