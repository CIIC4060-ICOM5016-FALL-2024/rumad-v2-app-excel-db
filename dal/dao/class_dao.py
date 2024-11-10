from dal.dao.dao import DAO

class ClassDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST ------------------------------------------------------------------------+
    def post_class(
        self,
        cid: int,
        cname: str,
        ccode: int,
        cdesc: str,
        term: str,
        years: str,
        cred: int,
        cysllabus: str,
    ):
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

    # PUT ------------------------------------------------------------------------+
    def put_class_by_cid(self, cid: int, data):
        """
        Updates a class tuple in the class relation
        :param cid: class id
        :param data: attributes to be updated
        :return: True if success, False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (cid,)
        query = f"UPDATE class SET {new} WHERE cid = %s"
        return self.update(query, values)

    # DELETE ------------------------------------------------------------------------+
    def delete_class_by_id(self, cid: int):
        """
        Deletes a tuple in the class relation
        :param cid: class id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM class WHERE cid = %s"
        value = [cid]
        return self.delete(query, value)

    # STATISTICS
    def get_top_classes_per_room(self, rid: int):
        """
        Gets all tuples from the class relation
        :param rid: academic room id
        :return: a list of tuples, or None if failed
        """
        # TODO FIX BY ROOM
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

    def get_top_classes_per_year(self, year: int, semester: str):
        """
        Gets top 3 classes per semester
        :param year: academic year
        :param semester: academic semester
        :return: a list of tuples, or None if failed
        """
        # TODO FIX BY YEAR SEMESTER
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
                SELECT COUNT(*), requisite.reqid, class.cdesc,class.ccode 
                FROM requisite INNER JOIN class ON requisite.reqid = class.cid 
                WHERE prereq = 'true' AND reqid != 37 
                GROUP BY requisite.reqid, class.cdesc,class.ccode
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