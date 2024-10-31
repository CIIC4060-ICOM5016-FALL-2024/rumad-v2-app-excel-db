from config.dbconfig import pg_config
import psycopg2


class DAO:
    def __init__(self):
        url = "dbname=%s password=%s host=%s port=%s user=%s" % (
            pg_config["dbname"],
            pg_config["password"],
            pg_config["host"],
            pg_config["port"],
            pg_config["user"],
        )
        self.connection = psycopg2.connect(url)

    # TODO Class CRUD

    # TODO Requisite CRUD

    # TODO Section CRUD
    def TopSectionStudent(self):
        cursor = self.connection.cursor()
        query = "SELECT s.sid, s.cid, r.building, r.room_number, s.capacity AS students_enrolled, r.capacity AS room_capacity, CAST(CAST(s.capacity AS decimal) / r.capacity AS decimal(20, 3)) AS student_to_capacity_ratio FROM section s JOIN room r ON s.roomid = r.rid GROUP BY s.sid, s.cid, r.building, r.room_number, s.capacity, r.capacity ORDER BY student_to_capacity_ratio DESC LIMIT 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

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
