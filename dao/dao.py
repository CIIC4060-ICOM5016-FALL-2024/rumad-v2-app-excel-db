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
        query = "select s.sid, s.cid, r.building, r.room_number, s.capacity as students_enrolled, r.capacity as room_capacity, CAST(CAST(s.capacity AS decimal) / r.capacity as decimal(20, 3)) as student_to_capacity_ratio from section s join room r ON s.roomid = r.rid group by s.sid, s.cid, r.building, r.room_number, s.capacity, r.capacity order by student_to_capacity_ratio desc limit 3;"
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
