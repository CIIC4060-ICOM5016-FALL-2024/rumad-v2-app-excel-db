from dao import DAO
from psycopg import sql

class RoomDAO(DAO):
    relation = 'room'

    def __init__(self):
        super().__init__()

    # POST
    def post_room(self, rid: int, building: str, room_number: int, capacity: int):
        """
        Creates a tuple in the room relation
        :param rid: room id
        :param building: building name
        :param room_number: room number
        :param capacity: maximum capacity of room
        :return: True if success, False otherwise
        """
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s)").
                 format(sql.Identifier(self.relation)))
        values = (rid, building, room_number, capacity)
        return self.create(query, values)

    # GET
    def get_all_rooms(self):
        """
        Gets all rows from the rooms relation
        :return: a list of tuples, or None if failed
        """
        query = ((sql.SQL("SELECT * FROM {}"))
                 .format(sql.Identifier(self.relation)))
        return self.read(query)

    def get_room_by_rid(self, rid: int):
        """
        Gets a row from the room relation, specified by rid
        :param rid: room id
        :return: a list with a single tuple, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation),
                         sql.Identifier('rid'), rid))
        return self.read(query)

    def get_top_rooms(self):
        # TODO Top 3 rooms with the most capacity
        # @Glorian
        return

    def get_top_rooms_in_building(self, building: str):
        # TODO Top 3 rooms with the most capacity in a building
        # @Glorian
        return

    def get_top_efficient_rooms(self):
        # TODO Top 3 rooms with the most student-to-capacity ratio
        return

    # PUT
    def put_room_rid(self, rid: int, rid_new: int):
        """
        Updates the rid of a tuple in the room relation specified by rid
        :param rid: room id
        :param rid_new: new room id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('rid'), rid_new),
                 sql.Identifier('rid'), rid)
        return self.update(query)

    def put_room_building(self, rid: int, building: str):
        """
        Updates the building of a tuple in the room relation specified by rid
        :param rid: room id
        :param building: building name
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('building'), building),
                 sql.Identifier('rid'), rid)
        return self.update(query)

    def put_room_number(self, rid: int, room_number: int):
        """
        Updates the room_number of a tuple in the room relation specified by rid
        :param rid: room id
        :param room_number: room number
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('room_number'), room_number),
                 sql.Identifier('rid'), rid)
        return self.update(query)

    def put_room_capacity(self, rid: int, capacity: int):
        """
        Updates the capacity of a tuple in the room relation specified by rid
        :param rid: room id
        :param capacity: maximum capacity of room
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('capacity'), capacity),
                 sql.Identifier('rid'), rid)
        return self.update(query)

    # DELETE
    def delete_room(self, rid: int):
        """
        Deletes a tuple in the meeting relation specified by rid
        :param rid: room id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('rid'), rid))
        return self.delete(query)


