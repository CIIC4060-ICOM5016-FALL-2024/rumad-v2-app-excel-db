from dal.dao.dao import DAO
from psycopg2 import sql


class SectionDAO(DAO):
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
        query = "INSERT INTO section VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = [sid, roomid, cid, mid, semester, years, capacity]
        return self.create(query, values)

    # GET
    def get_all_sections(self):
        """
        Gets all tuples from the section relation
        :return: a list of tuples, or None if failed.
        """
        query = "SELECT * FROM section"
        return self.read(query)

    def get_section_by_sid(self, sid: int):
        """
        Gets a tuple from the section relation
        :param sid: section id
        :return: a list with a single tuple, or None if failed.
        """
        query = "SELECT * FROM section WHERE sid = %s"
        return self.read(query, [sid, ])

    # PUT
    def put_section_by_sid(self, sid: int, data):
        """
        Updates the sid of a tuple in the section relation
        :param sid: section id
        :param sid_new: new section id
        :return: True if success, false otherwise.
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        params = tuple(data.values()) + (sid, )
        query = f"UPDATE section SET {new} WHERE sid = %s"
        values = [params]
        return self.update(query, values)

    # DELETE
    def delete_section(self, sid: int):
        """
        Deletes a tuple in the section relation
        :param sid: section id
        :return: True if success, false otherwise.
        """
        query = "DELETE FROM section WHERE sid = %s"
        values = [sid]
        return self.delete(query, values)

    # STATISTICS
    def get_sections_per_year(self):
        """
        Gets all tuples from the section relation
        :return: a list of tuples, or None if failed.
        """
        query = """
                 SELECT years AS year, COUNT(*) AS total_sections 
                 FROM section 
                 GROUP BY years 
                 ORDER BY total_sections;
         """
        return self.read(query)

