from dao import DAO
from psycopg import sql


class SectionDAO(DAO):
    relation = 'section'

    def __init__(self):
        super().__init__()

    # POST
    def post_section(self, sid: int, roomid: int, cid: int, mid: int, semester: str, years: int, capacity: int):
        """
        Creates a tuple in the section relation
        :param sid: section id
        :param roomid: room id
        :param cid: course id
        :param mid: meeting id
        :param semester: Fall, Spring, V1 or V2
        :param years: academic year
        :param capacity: number of enrolled students
        :return: True if success, False otherwise
        """
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s)").
                 format(sql.Identifier(self.relation)))
        values = [sid, roomid, cid, mid, semester, years, capacity]
        return self.create(query, values)

    # GET
    def get_all_sections(self):
        """
        Gets all tuples from the section relation
        :return: a list of tuples, or None if failed.
        """
        query = (sql.SQL("SELECT * FROM {}").
                 format(sql.Identifier(self.relation)))
        return self.read(query)

    def get_section_by_sid(self, sid: int):
        """
        Gets a tuple from the section relation
        :param sid: section id
        :return: a list with a single tuple, or None if failed.
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = {}").format
                 (sql.Identifier(self.relation), sql.Identifier('sid'), sid))
        return self.read(query)

    def get_top_3_section(self):
        # TODO Top 3 sections with the most student-to-capacity ratio.
        # @Glorian
        return

    def get_sections_per_year(self, year: int):
        # TODO Total number of sections per year
        return
    # PUT
    def put_section_sid(self, sid: int, sid_new: int):
        """
        Updates the sid of a tuple in the section relation
        :param sid: section id
        :param sid_new: new section id
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('sid'), sid_new,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_roomdid(self, sid: int, roomid: int):
        """
        Updates the roomid of a tuple in the section relation
        :param sid: section id
        :param roomid: room id
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('roomid'), roomid,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_cid(self, sid: int, cid: int):
        """
        Updates the cid of a tuple in the section relation
        :param sid: section id
        :param cid: course id
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cid'), cid,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_mid(self, sid: int, mid: int):
        """
        Updates the mid of a tuple in the section relation
        :param sid: section id
        :param mid: meeting id
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('mid'), mid,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_semester(self, sid: int, semester: str):
        """
        Updates the semester of a tuple in the section relation
        :param sid: section id
        :param semester: Fall, Spring, V1 or V2
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('semester'), semester,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_years(self, sid: int, years: int):
        """
        Updates the years of a tuple in the section relation
        :param sid: section id
        :param years: academic year
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('years'), years,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    def put_section_capacity(self, sid: int, capacity: int):
        """
        Updates the capacity of a tuple in the section relation
        :param sid: section id
        :param capacity: number of students enrolled
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('capacity'), capacity,
                         sql.Identifier('sid'), sid))
        return self.update(query)

    # DELETE
    def delete_section(self, sid: int):
        """
        Deletes a tuple in the section relation
        :param sid: section id
        :return: True if success, false otherwise.
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('sid'), sid))
        return self.delete(query)

