from model.section_dao import SectionDAO
from model.class_dao import ClassDAO
from model.meeting_dao import MeetingDAO
from model.room_dao import RoomDAO
from handler.room_handler import Room_Handler
from handler.class_handler import Class_Handler
from handler.meeting_handler import Meeting_Handler
from flask import jsonify

class Statistics_Controller:

    def __init__(self):
        pass

    """ LOCAL STATISTICS """
    def top_room_capacity_by_building(self, building):
        dao = RoomDAO()
        rooms = dao.get_top_rooms_in_building(building)
        return Room_Handler.result_room(rooms)

    def top_ratio_rooms(self, id):
        dao = RoomDAO()
        rooms = dao.get_top_ratio_rooms(id)
        return Room_Handler.result_room(rooms)

    def top_classes_per_room(self, id):
        dao = ClassDAO()
        classes = dao.get_top_classes_per_room(id)
        return Class_Handler.result_class(classes)

    def top_classes_per_semester(self, year, semester):
        dao = ClassDAO()
        classes = dao.get_top_classes_per_year(year, semester)
        return Class_Handler.result_class(classes)

    """ GLOBAL STATISTICS """
    def top_meeting(self):
        dao = MeetingDAO()
        meetings = dao.get_top_meetings()
        return Meeting_Handler.result_meeting(meetings)

    def top_pre_requisite(self):
        result = []
        dao = ClassDAO()
        requisites = dao.get_top_prerequisites()
        if requisites:
            for item in requisites:
                result_dict = {"count": item[0], "requid": item[1], "cdesc": item[2], "ccode": item[3]}
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def top_least_classes(self):
        result = []
        dao = ClassDAO()
        classes = dao.get_least_classes()
        if classes:
            for item in classes:
                result_dict = {"cid": item[0], "count": item[1], "cdesc": item[2]}
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def total_sections(self):
        dao = SectionDAO()
        result = []
        sections = dao.get_sections_per_year()
        if sections:
            for item in sections:
                result_dict = {"year": item[0], "total_sections": item[1]}
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404
