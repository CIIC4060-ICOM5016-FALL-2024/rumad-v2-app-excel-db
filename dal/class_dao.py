from dal.dao import DAO

class ClassDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST ------------------------------------------------------------------------+
    def post_class(
        self,
        cname: str,
        ccode: int,
        cdesc: str,
        term: str,
        years: str,
        cred: int,
        csyllabus: str,
    ):
        """
        Creates a tuple in the class relation
        :param cname: class name
        :param ccode: class code
        :param cdesc: class description
        :param term: academic term
        :param years: academic years
        :param cred: credit
        :param csyllabus: class syllabus
        :return: True if success, False otherwise
        """
        query = """
        INSERT INTO class (cname, ccode, cdesc, term, years, cred, csyllabus) 
        VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING cid;
        """
        values = [cname, ccode, cdesc, term, years, cred, csyllabus]
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
        Gets the top 3 most given classes in a room
        :param rid: the room id
        :return: a list of tuples, or a False inside a tuple if failed.
        """
        query = """
            SELECT class.cid, cname, ccode, cdesc, term, years, cred, csyllabus, amount
            FROM (
                  SELECT cid, count(*) AS amount
                  FROM section
                  WHERE roomid = %s
                  GROUP BY cid
                  ORDER BY amount DESC
                  LIMIT 3
            )
            AS per_room, class
            WHERE class.cid = per_room.cid
            ORDER BY amount DESC
        """
        return self.read(query, [rid])

    def get_top_classes_per_year(self, year: int, semester: str):
        """
        Gets top 3 classes per semester and year
        :param year: academic year
        :param semester: academic semester
        :return: a list of tuples, or None if failed
        """
        query = """
                SELECT class.cid, cname, ccode, cdesc, term, years, cred, csyllabus,section_amount
                FROM (SELECT cid, count(*) AS section_amount
                      FROM section
                      WHERE semester ILIKE %s
                        AND years = %s
                      GROUP BY cid
                      ORDER BY section_amount DESC
                      LIMIT 3
                ) as cid_per_semester, class
                where class.cid = cid_per_semester.cid order by section_amount desc;
        """
        values = [semester, year]
        return self.read(query, values)

    def get_top_prerequisites(self):
        """
        Gets top 3 classes that appears the most as prerequisite to other classes.
        :return: a list of tuples, or a tuple with False if failed
        """
        query = """
        SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus, frequency
        FROM(SELECT reqid, count(reqid) AS frequency
            FROM requisite WHERE prereq = true
            GROUP BY reqid
            ORDER BY frequency DESC
            LIMIT 3)
        AS prereq, class WHERE reqid = cid
        ORDER BY frequency DESC;
        """
        return self.read(query)

    def get_least_classes(self):
        """
        Gets the top 3 least given classes.
        :return: a list of tuples, or a tuple with False if failed
        """
        query = """
        SELECT cid, cname, ccode, cdesc, term, years, cred, csyllabus, frequency
        FROM
            (SELECT cid, count(cid) AS frequency
            FROM class JOIN section USING (cid)
            GROUP BY cid
            ORDER BY cid) AS least 
            NATURAL JOIN class
        ORDER BY frequency
        LIMIT 3;
        """
        return self.read(query)