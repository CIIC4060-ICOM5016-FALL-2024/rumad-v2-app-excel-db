from dal.dao.dao import DAO
from datetime import datetime


class MeetingDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_meeting(
        self, mid: int, ccode: int, start_time: datetime, end_time: datetime, cdays
    ):
        """
        Creates a tuple in the meeting relation
        :param mid: meeting id
        :param ccode: course code
        :param start_time: start of the meeting
        :param end_time: end of the meeting
        :return: True if success, False otherwise
        """
        query = "INSERT INTO meeting VALUES (%s, %s, %s, %s, %s)"
        values = [mid, ccode, start_time, end_time, cdays]
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

    # PUT
    def put_meeting_by_mid(self, mid: int, data):
        """
        Updates a meeting tuple in the meeting relation
        :param mid: meeting id
        :param data: attributes to be updated
        :return: True if success, False otherwise
        """
        new = ", ".join([f"{key} = %s" for key in data.keys()])
        params = tuple(data.values()) + (mid,)
        query = f"UPDATE meeting SET {new} WHERE mid = %s"
        values = [params]
        return self.update(query, values)

    # DELETE
    def delete_meeting(self, mid: int):
        """
        Deletes a tuple in meeting relation
        :param mid: meeting id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM meeting WHERE mid = %s"
        values = [mid]
        return self.delete(query, values)

    # STATISTICS
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
