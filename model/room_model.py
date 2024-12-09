from dal.room_dao import RoomDAO
from flask import jsonify

attributes = ["building", "room_number", "capacity"]


class RoomModel:

    def __init__(self):
        pass

    @staticmethod
    def jsonify_response(response):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """

        if False in response:
            return (
                jsonify(f"The requested room with ID {response[1]} was not found."),
                404,
            )  # not found

        result = []

        for room in response:
            result_dict = {
                "rid": room[0],
                "building": room[1],
                "room_number": room[2],
                "capacity": room[3],
            }

            result.append(result_dict)

        return jsonify(result), 200

    def get_all_rooms(self):
        """
        Gets all rooms from the room relation database.
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.get_all_rooms()
        return self.jsonify_response(response)

    @staticmethod
    def post_rooms(data):
        """
        Creates a new room tuple in the room relation database.
        @param data: a list with attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            room_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f"Missing required attribute: {missing_attribute}"), 400

        building = room_attributes["building"]
        room_number = room_attributes["room_number"]
        capacity = room_attributes["capacity"]

        dao = RoomDAO()

        response = dao.post_room(building, room_number, capacity)

        if False in response:
            return jsonify(f"Could not create room {room_number} in {building}."), 400

        return (
            jsonify(
                f"Room {room_number} in {building} has been created with rid {response[1]}."
            ),
            201,
        )

    def get_room_by_id(self, rid):
        """
        Gets a room by its rid
        @param rid: room id
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.get_room_by_rid(rid)
        return self.jsonify_response(response)

    @staticmethod
    def put_room_by_id(rid, data):
        """
        Updates a room by its rid
        @param rid: room id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.put_room_by_rid(rid, data)

        if False in response:
            return jsonify(f"Failed to update room with ID {rid}."), 400
        return jsonify(f"Room {rid} has been updated."), 200

    @staticmethod
    def delete_room_by_id(rid):
        """
        Deletes a room by its rid
        @param rid: room id
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.delete_room(rid)

        if False in response:
            return jsonify(f"Could not delete room with ID {rid}."), 400
        return jsonify(f"Room {rid} has been deleted."), 200
