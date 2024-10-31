from config.dbconfig import pg_config
import psycopg

# HEAVY ERROR HANDLING HERE AND HERE ONLY.
# MOST FAILURES WOULD OCCUR HERE LIKE
# FAILED CONNECTIONS, BAD QUERIES, TIMEOUTS AND WHATEVER

class DAO:
    connection = None

    def __init__(self):
        self.url = ("dbname=%s password=%s host=%s port=%s user=%s" %
                    (pg_config['dbname'],
                     pg_config['password'],
                     pg_config['host'],
                     pg_config['port'],
                     pg_config['user'])
                    )

    def connect(self):
        try:
            self.connection = psycopg.connect(self.url)
        except (Exception, psycopg.DatabaseError) as error:
            print(error)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def execute(self, sql, args):
        if self.connection is not None:
            cursor = self.connection.cursor()
            cursor.execute(sql, args)
            cursor.close()
            return cursor

    def cursor(self):
        return self.connection.cursor()

    def create(self):
        pass

    def read(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
