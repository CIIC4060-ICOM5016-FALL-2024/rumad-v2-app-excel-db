from dao import DAO
from psycopg2 import sql

class ClassDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST ------------------------------------------------------------------------+
    def post_class(self, cid: int, cname: str, ccode: int,
                   cdesc: str, term: str, years: str, cred: int, cysllabus: str):
        """
        Creates a tuple in the class relation
        :param cid: class id
        :param cname: class name
        :param ccode: class code
        :param cdesc: class description
        :param term: academic term
        :param years: academic years
        :param cred: credit
        :param cysllabus: class syllabus
        :return: True if success, False otherwise
        """
        query = "INSERT INTO class VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        values = [cid, cname, ccode, cdesc, term, years, cred, cysllabus]
        return self.create(query, values)

    # GET ------------------------------------------------------------------------+
    def get_all_classes(self):
        """
        Gets all tuples from the class relation
        :return: a list of tuples, or None if failed
        """
        query = "SELECT * FROM class"
        return self.read(query)

    def get_class_by_cid(self, cid: int):
        """
        Gets a tuple from the class relation
        :param cid: class id
        :return: a list with a single tuple, or None if failed
        """
        query = "SELECT * FROM class WHERE cid = %s"
        values = [cid]
        return self.read(query, values)

    def get_top_classes(self, year: int, semester: str):
        """
        Gets top 3 classes per semester
        :param year: academic year
        :param semester: academic semester
        :return: a list of tuples, or None if failed
        """
        query = """
                SELECT class.cid, cname, ccode, cdesc, semester, must_cid_per_semester.section_count
                FROM (
                      SELECT sec1.cid, sec1.semester, COUNT(*) AS section_count
                      FROM section AS sec1
                      GROUP BY sec1.cid, sec1.semester
                      HAVING (sec1.cid, sec1.semester) IN (
                           SELECT sec2.cid, sec2.semester
                           FROM section as sec2
                           WHERE sec2.semester = sec1.semester
                           GROUP BY sec2.cid, sec2.semester
                           ORDER BY COUNT(*) DESC
                           LIMIT 3
                      )
                      ORDER BY section_count DESC, sec1.semester
                ) AS must_cid_per_semester
                JOIN class ON must_cid_per_semester.cid = class.cid
                ORDER BY section_count DESC;
        """
        return self.read(query)

    def get_top_prerequisites(self):
        """
        Gets all tuples from the class relation
        :return: a list of tuples, or None if failed
        """
        query = """
                SELECT COUNT(*), requisite.reqid, class.cdesc 
                FROM requisite INNER JOIN class ON requisite.reqid = class.cid 
                WHERE prereq = 'true' AND reqid != 37 
                GROUP BY requisite.reqid, class.cdesc 
                ORDER BY COUNT(*) DESC limit 3;
        """
        return self.read(query)

    def get_least_classes(self):
        """
        Gets all tuples from the class relation
        :return: a list of tuples, or None if failed
        """
        query = """
                SELECT DISTINCT section.cid,count(*) AS section_count, class.cdesc 
                FROM section INNER JOIN class ON section.cid = class.cid 
                GROUP BY section.cid , class.cdesc 
                ORDER BY section_count limit 3;
        """
        return self.read(query)

    def get_top_classes_in_room(self, rid: int):
        """
        Gets all tuples from the class relation
        :param rid: academic room id
        :return: a list of tuples, or None if failed
        """
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
        return self.read(query)

    # PUT ------------------------------------------------------------------------+
    def put_class_cid(self, cid: int, cid_new: int):
        """
        Updates the cid of a tuple in the class relation
        :param cid: class id
        :param cid_new: new class id
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET cid = %s WHERE cid = %s"
        values = [cid_new, cid]
        return self.update(query, values)

    def put_class_cname(self, cid: int, cname: str):
        """
        Updates the cname of a tuple in the class relation
        :param cid: class id
        :param cname: new class name
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET cname = %s WHERE cid = %s"
        values = [cname, cid]
        return self.update(query, values)

    def put_class_ccode(self, cid: int, ccode: int):
        """
        Updates the ccode of a tuple in the class relation
        :param cid: class id
        :param ccode: new class code
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET ccode = %s WHERE cid = %s"
        values = [ccode, cid]
        return self.update(query, values)

    def put_class_cdesc(self, cid: int, cdesc: str):
        """
        Updates the cdesc of a tuple in the class relation
        :param cid: class id
        :param cdesc: new class description
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET cdesc = %s WHERE cid = %s"
        values = [cdesc, cid]
        return self.update(query, values)

    def put_class_term(self, cid: int, term: str):
        """
        Updates the term of a tuple in the class relation
        :param cid: class id
        :param term: new academic term
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET term = %s WHERE cid = %s"
        values = [term, cid]
        return self.update(query, values)

    def put_class_years(self, cid: int, years: str):
        """
        Updates the years of a tuple in the class relation
        :param cid: class id
        :param years: new academic years
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET years = %s WHERE cid = %s"
        value = [years, cid]
        return self.update(query, value)

    def put_class_cred(self, cid: int, cred: int):
        """
        Updates the creds of a tuple in the class relation
        :param cid: class id
        :param cred: new credits
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET cred = %s WHERE cid = %s"
        value = [cred, cid]
        return self.update(query, value)

    def put_class_csyllabus(self, cid: int, csyllabus: str):
        """
        Updates the csyllabus of a tuple in the class relation
        :param cid: class id
        :param csyllabus: new syllabus
        :return: True if success, False otherwise
        """
        query = "UPDATE class SET csyllabus = %s WHERE cid = %s"
        value = [csyllabus, cid]
        return self.update(query, value)

    # DELETE ------------------------------------------------------------------------+
    def delete_class(self, cid: int):
        """
        Deletes a tuple in the class relation
        :param cid: class id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM class WHERE cid = %s"
        value = [cid]
        return self.delete(query, value)
