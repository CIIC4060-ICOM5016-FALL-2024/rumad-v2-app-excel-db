from config.dbconfig import pg_config
import psycopg2

class DAO:
    def __init__(self):
        url = ("dbname=%s password=%s host=%s port=%s user=%s" %
               (pg_config['dbname'],
                pg_config['password'],
                pg_config['host'],
                pg_config['port'],
                pg_config['user'])
               )
        self.connection = psycopg2.connect(url)

    # TODO Class CRUD

    # TODO Requisite CRUD

    # TODO Section CRUD

    # TODO Meeting CRUD

    # TODO Room CRUD
    def TopRoomCapacity(self):
        cursor = self.connection.cursor()
        query = "select rid, building, room_number, capacity from room order by capacity desc limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result