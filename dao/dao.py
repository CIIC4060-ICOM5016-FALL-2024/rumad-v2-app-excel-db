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

    def TopClassesSemesterDAO(self):
        # TODO Top 3 most taught classes per semester.
        # @Alanis
        cur = self.connection.cursor()
        query = """
                
                """
        return

    def topClassesRoom(self):
        # Top 3 classes that were taught the most per room.
        # @Alanis
        cur = self.connection.cursor()
        query = """
                SELECT cname, ccode, cdesc, building, room_number,cid_per_room.amount
                FROM (
                    SELECT DISTINCT sec2.cid, sec2.roomid, sec1.amount
                    FROM (
                        SELECT roomid, COUNT(*) AS amount
                        FROM section
                        GROUP BY roomid
                    ) AS sec1
                    JOIN section AS sec2 ON sec1.roomid = sec2.roomid
                    WHERE sec2.cid IN (
                        SELECT sec3.cid
                        FROM section as sec3
                        WHERE sec3.roomid = sec2.roomid
                        ORDER BY sec3.cid
                        LIMIT 3
                    )
                    ORDER BY sec1.amount DESC, sec2.roomid, sec2.cid
                ) AS cid_per_room
                JOIN class ON cid_per_room.cid = class.cid
                JOIN room ON cid_per_room.roomid = room.rid
                ORDER BY amount DESC
        """
        cur.execute(query)
        result = []
        for row in cur.fetchall():
            result.append(row)
        return result

    # Global Statistics ---------------------------------------------+
    def TopMeetingsSemesterDAO(self):
        # TODO Top 5 meetings with the most sections.
        # @Alanis
        return

    # TODO Class CRUD

    # TODO Requisite CRUD

    # TODO Section CRUD

    # TODO Meeting CRUD

    # TODO Room CRUD