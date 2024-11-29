from dal.dao import DAO

class RoomDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_room(self, building: str, room_number: int, capacity: int):
        """
        Creates a tuple in the room relation
        :param building: building name
        :param room_number: room number
        :param capacity: maximum capacity of room
        :return: True if success, False otherwise
        """
        query = """INSERT INTO room (building, room_number, capacity)
        VALUES (%s, %s, %s) RETURNING rid
        """
        values = (building, room_number, capacity)
        return self.create(query, values)

    # GET
    def get_all_rooms(self):
        """
        Gets all rows from the rooms relation
        :return: a list of tuples, or None if failed
        """
        query = "SELECT * FROM room"
        return self.read(query)

    def get_room_by_rid(self, rid: int):
        """
        Gets a row from the room relation, specified by rid
        :param rid: room id
        :return: a list with a single tuple, or None if failed
        """
        query = "SELECT * FROM room WHERE rid = %s"
        values = [rid]
        return self.read(query, values)

    # PUT
    def put_room_by_rid(self, rid: int, data):
        """
        Updates a room tuple in the room relation
        :param rid: room id
        :param data: attributes to be updated
        :return: True if success, False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (rid, )
        query = f"UPDATE room SET {new} WHERE rid = %s"
        return self.update(query, values)

    # DELETE
    def delete_room(self, rid: int):
        """
        Deletes a tuple in the meeting relation specified by rid
        :param rid: room id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM room WHERE rid = %s"
        values = [rid]
        return self.delete(query, values)

    # STATISTICS
    def get_top_rooms_in_building(self, building: str):
        """
        Gets the top 3 rooms with the most capacity in a building
        :return: a list of tuples, or False inside a tuple if failed
        """
        query = """
                SELECT rid, building, room_number, capacity 
                FROM room 
                WHERE building ILIKE %s
                ORDER BY capacity DESC limit 3;
                """
        values = [building]
        return self.read(query, values)

    def get_top_ratio_rooms(self, building: str):
        """
        Gets the top 3 rooms with the most student to capacity ratio.
        :return: a list of tuples, or False inside a tuple if failed
        """
        query = """
        SELECT rid, building, room_number, room.capacity,
        CAST(students AS FLOAT) / CAST(seats AS FLOAT) AS ratio
        FROM (SELECT rid, room.capacity AS seats, avg(section.capacity) AS students
            FROM section, room
            WHERE roomid = rid
            AND building ILIKE %s
            GROUP BY rid) AS sums
        NATURAL JOIN room
        ORDER BY ratio DESC
        LIMIT 3;
        """
        values = [building]
        return self.read(query, values)
