from dao import DAO
from psycopg import sql
from datetime import datetime

class MeetingDAO(DAO):
    relation = 'meeting'

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
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s)").
                 format(sql.Identifier(self.relation)))
        values = (mid, ccode, start_time, end_time)
        return self.create(query, values)

    # GET
    def get_all_meetings(self):
        """
        Gets all tuples from the meeting relation
        :return: a list of tuples, or None if failed
        """
        query = ((sql.SQL("SELECT * FROM {}"))
                 .format(sql.Identifier(self.relation)))
        return self.read(query)

    def get_meeting_by_mid(self, mid: int):
        """
        Gets a tuple from the meeting relation
        :param mid: meeting id
        :return: a list with a single tuple, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation),
                         sql.Identifier('mid'), mid))
        return self.read(query)

    # PUT
    def put_meeting_mid(self, mid: int, mid_new: int):
        """
        Updates the mid of a tuple in the meeting relation
        :param mid: meeting id
        :param mid_new: new meeting id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('mid'), mid_new),
                 sql.Identifier('mid'), mid)
        return self.update(query)

    def put_meeting_ccode(self, mid: int, ccode: int):
        """
        Updates the ccode of a tuple in the meeting relation
        :param mid: meeting id
        :param ccode: course code
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('ccode'), ccode),
                 sql.Identifier('mid'), mid)
        return self.update(query)

    def put_meeting_start_time(self, mid: int, start_time: datetime):
        """
        Updates the start_time of a tuple in the meeting relation
        :param mid: meeting id
        :param start_time: start of the meeting
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('start_time'), start_time,
                        sql.Identifier('mid'), mid))
        return self.update(query)

    def put_meeting_end_time(self, mid: int, end_time: datetime):
        """
        Updates the end_time of a tuple in the meeting relation
        :param mid: meeting id
        :param end_time: end of the meeting
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('end_time'), end_time,
                        sql.Identifier('mid'), mid))
        return self.update(query)

    def put_meeting_cdays(self, mid: int, cdays: str):
        """
        Updates the cdays of a tuple in the meeting relation
        :param mid: meeting id
        :param cdays: course days
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('cdays'), cdays,
                        sql.Identifier('mid'), mid))
        return self.update(query)

    # DELETE
    def delete_meeting(self, mid: int):
        """
        Deletes a tuple in meeting relation
        :param mid: meeting id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('mid'), mid))
        return self.delete(query)


