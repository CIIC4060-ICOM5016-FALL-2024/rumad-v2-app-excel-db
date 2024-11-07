from dao import DAO
from psycopg2 import sql
from datetime import datetime

class MeetingDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_meeting(self, mid: int, ccode: int, start_time: datetime, end_time: datetime):
        """
        Creates a tuple in the meeting relation
        :param mid: meeting id
        :param ccode: course code
        :param start_time: start of the meeting
        :param end_time: end of the meeting
        :return: True if success, False otherwise
        """
        query = "INSERT INTO meeting VALUES (%s, %s, %s, %s, %s)"
        values = [mid, ccode, start_time, end_time]
        return self.create(query, values)

    # GET
    def get_all_meetings(self):
        """
        Gets all tuples from the meeting relation
        :return: a list of tuples, or None if failed
        """
        query = "SELECT * FROM meeting"
        return self.read(query)

    def get_meeting_by_mid(self, mid: int):
        """
        Gets a tuple from the meeting relation
        :param mid: meeting id
        :return: a list with a single tuple, or None if failed
        """
        query = "SELECT * FROM meeting WHERE mid = %s"
        value = [mid]
        return self.read(query, value)

    def get_top_meetings(self):
        """
        Gets all tuples from the meeting relation
        :return: a list of tuples, or None if failed
        """
        query = """
                SELECT meeting.mid, meeting.starttime, meeting.endtime, meeting.cdays, section_amount
                FROM (SELECT mid, COUNT(*) AS section_amount
                      FROM section
                      group by mid
                      ORDER BY section_amount DESC, mid
                      LIMIT 5) as section
                JOIN meeting ON section.mid = meeting.mid
        """
        return self.read(query)

    # PUT
    def put_meeting_mid(self, mid: int, mid_new: int):
        """
        Updates the mid of a tuple in the meeting relation
        :param mid: meeting id
        :param mid_new: new meeting id
        :return: True if success, False otherwise
        """
        query = "UPDATE meeting SET mid = %s WHERE mid = %s"
        value = [mid_new, mid]
        return self.update(query, value)

    def put_meeting_ccode(self, mid: int, ccode: int):
        """
        Updates the ccode of a tuple in the meeting relation
        :param mid: meeting id
        :param ccode: course code
        :return: True if success, False otherwise
        """
        query = "UPDATE meeting SET ccode = %s WHERE mid = %s"
        values = [ccode, mid]
        return self.update(query, values)

    def put_meeting_start_time(self, mid: int, start_time: datetime):
        """
        Updates the start_time of a tuple in the meeting relation
        :param mid: meeting id
        :param start_time: start of the meeting
        :return: True if success, False otherwise
        """
        query = "UPDATE meeting SET starttime = %s WHERE mid = %s"
        values = [start_time, mid]
        return self.update(query, values)

    def put_meeting_end_time(self, mid: int, end_time: datetime):
        """
        Updates the end_time of a tuple in the meeting relation
        :param mid: meeting id
        :param end_time: end of the meeting
        :return: True if success, False otherwise
        """
        query = "UPDATE meeting SET endtime = %s WHERE mid = %s"
        values = [end_time, mid]
        return self.update(query, values)

    def put_meeting_cdays(self, mid: int, cdays: str):
        """
        Updates the cdays of a tuple in the meeting relation
        :param mid: meeting id
        :param cdays: course days
        :return: True if success, False otherwise
        """
        query = "UPDATE meeting SET cdays = %s WHERE mid = %s"
        values = [cdays, mid]
        return self.update(query, values)

    # DELETE
    def delete_meeting(self, mid: int):
        """
        Deletes a tuple in meeting relation
        :param mid: meeting id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM meeting WHERE mid = %s"
        values = [mid, ]
        return self.delete(query, values)


