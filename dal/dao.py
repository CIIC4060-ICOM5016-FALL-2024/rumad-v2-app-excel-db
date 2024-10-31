from config.dbconfig import pg_config
import psycopg
from psycopg_pool import ConnectionPool

url = ("dbname=%s password=%s host=%s port=%s user=%s" %
            (pg_config['dbname'],
             pg_config['password'],
             pg_config['host'],
             pg_config['port'],
             pg_config['user']))

pool = ConnectionPool(url)


# HEAVY ERROR HANDLING HERE AND HERE ONLY.
# MOST FAILURES WOULD OCCUR HERE LIKE
# FAILED CONNECTIONS, BAD QUERIES, TIMEOUTS AND WHATEVER

class DAO:

    def __init__(self):
        self.pool = pool

    def cursor(self):
        with self.pool.connection() as conn:
            return conn.cursor()

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass


