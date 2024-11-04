from dao import DAO
from psycopg2 import sql


class ClassDAO(DAO):
    relation = 'class'

    def __init__(self):
        super().__init__()

    # POST
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
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                 .format(sql.Identifier(self.relation)))
        values = [cid, cname, ccode, cdesc, term, years, cred, cysllabus]
        return self.create(query, values)

    # GET
    def get_all_classes(self):
        """
        Gets all tuples from the class relation
        :return: a list of tuples, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {}")
                 .format(sql.Identifier(self.relation)))

        return self.read(query)

    def get_class_by_cid(self, cid: int):
        """
        Gets a tuple from the class relation
        :param cid: class id
        :return: a list with a single tuple, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('cid')))

        values = [cid, ]

        return self.read(query, values)

    def get_top_classes(self, year: int, semester: str):
        cur = self.pool.getconn().cursor()
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
                ORDER BY section_count DESC
                """
        cur.execute(query)
        result = []
        for row in cur.fetchall():
            result.append(row)
        return result

    def get_top_prerequisites(self):
        cursor = self.pool.getconn().cursor()
        query = "select count(*), requisite.requid, class.cdesc from requisite inner join class on requisite.requid = class.cid where prereq = 'true' and requid != 37 group by requisite.requid, class.cdesc order by count(*) desc limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def get_least_classes(self):
        cursor = self.pool.getconn().cursor()
        query = "select distinct section.cid,count(*) as section_count, class.cdesc from section inner join class on section.cid = class.cid group by section.cid , class.cdesc order by section_count limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def get_top_classes_in_room(self, rid: int):
        cur = self.pool.getconn().cursor()
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

    # PUT
    def put_class_cid(self, cid: int, cid_new: int):
        """
        Updates the cid of a tuple in the class relation
        :param cid: class id
        :param cid_new: new class id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('cid'),
                         sql.Identifier('cid')))

        values = [cid_new, cid]

        return self.update(query, values)

    def put_class_cname(self, cid: int, cname: str):
        """
        Updates the cname of a tuple in the class relation
        :param cid: class id
        :param cname: new class name
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('cname'),
                         sql.Identifier('cid')))

        values = [cname, cid]

        return self.update(query, values)

    def put_class_ccode(self, cid: int, ccode: int):
        """
        Updates the ccode of a tuple in the class relation
        :param cid: class id
        :param ccode: new class code
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('ccode'),
                         sql.Identifier('cid')))
        values = [ccode, cid]
        return self.update(query, values)

    def put_class_cdesc(self, cid: int, cdesc: str):
        """
        Updates the cdesc of a tuple in the class relation
        :param cid: class id
        :param cdesc: new class description
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('cdesc'),
                         sql.Identifier('cid')))

        values = [cdesc, cid]

        return self.update(query)

    def put_class_term(self, cid: int, term: str):
        """
        Updates the term of a tuple in the class relation
        :param cid: class id
        :param term: new academic term
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('term'),
                         sql.Identifier('cid')))
        values = [term, cid]

        return self.update(query, values)

    def put_class_years(self, cid: int, years: str):
        """
        Updates the years of a tuple in the class relation
        :param cid: class id
        :param years: new academic years
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('years'),
                         sql.Identifier('cid')))

        value = [years, cid]

        return self.update(query, value)

    def put_class_cred(self, cid: int, cred: int):
        """
        Updates the creds of a tuple in the class relation
        :param cid: class id
        :param cred: new credits
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('cred'),
                         sql.Identifier('cid')))

        value = [cred, cid]

        return self.update(query, value)

    def put_class_csyllabus(self, cid: int, csyllabus: str):
        """
        Updates the csyllabus of a tuple in the class relation
        :param cid: class id
        :param csyllabus: new syllabus
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = %s WHERE {} = %s")
                 .format(sql.Identifier(self.relation), sql.Identifier('csyllabus'),
                         sql.Identifier('cid')))
        value = [csyllabus, cid]

        return self.update(query, value)

    # DELETE
    def delete_class(self, cid: int):
        """
        Deletes a tuple in the class relation
        :param cid: class id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = %s").
                 format(sql.Identifier(self.relation), sql.Identifier('cid')))
        value = [cid, ]
        return self.delete(query, value)
