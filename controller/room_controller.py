from model.room_dao import RoomDAO
from flask import jsonify

class Room_Controller:

    def __init__(self):
        pass

    def result_room(rooms):
        result = []
        if rooms:
            for item in rooms:
                result_dict = {
                    "rid": item[0],
                    "building": item[1],
                    "room_number": item[2],
                    "capacity": item[3],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404
    
    def get_rooms(self):
        dao = RoomDAO()
        rooms = dao.get_all_rooms()
        return self.result_room(rooms)

    def post_rooms(self, data):
        dao = RoomDAO()
        building = data["building"]
        room_number = data["room_number"]
        capacity = data["capacity"]
        if dao.post_room(building, room_number, capacity):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_room_by_id(self, rid):
        dao = RoomDAO()
        room = dao.get_room_by_rid(rid)
        return self.result_room(room)

    def put_room_by_id(self, rid, data):
        dao = RoomDAO()
        if dao.put_room_by_rid(int(rid), data):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def delete_room_by_id(self, rid):
        dao = RoomDAO()
        if dao.delete_room(rid):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404