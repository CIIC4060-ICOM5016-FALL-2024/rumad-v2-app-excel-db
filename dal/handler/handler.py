from dal.dao.class_dao import ClassDAO
from dal.dao.meeting_dao import MeetingDAO
from dal.dao.room_dao import RoomDAO
from dal.dao.section_dao import SectionDAO

from flask import jsonify

class Handler:
    def __init__(self):
        pass

    def top_room_capacity(self):
        result = []
        dao = RoomDAO()
        temp = dao.get_top_rooms()
        if temp:
            for tuple in temp:
                temp_dict = {}
                temp_dict['sid'] = tuple[0]
                temp_dict['cid'] = tuple[1]
                temp_dict['building'] = tuple[2]
                temp_dict['room_number'] = tuple[3]
                temp_dict['students_enrolled'] = tuple[4]
                temp_dict['room_capacity'] = tuple[5]
                temp_dict['student_to_capacity_ratio'] = tuple[6]
                result.append(temp_dict)
        else:
            return jsonify("Error not executed"), 404
        return jsonify(result)

    def top_section_student(self):
        result = []
        dao = RoomDAO()
        temp = dao.get_top_efficient_rooms()
        if temp:
            for tuple in temp:
                temp_dict = {}
                temp_dict['rid'] = tuple[0]
                temp_dict['building'] = tuple [1]
                temp_dict['room_number'] = tuple[2]
                temp_dict['capacity'] = tuple [3]
                result.append(temp_dict)
        else:
            return jsonify("Error not executed"), 404
        return jsonify(result)

    def topClassesSemester(self):
        # TODO Top 3 most taught classes per semester
        # @Alanis
        # return ClassDAO().get_top_classes()
        pass

    def topClassesRoom(self):
        # TODO Top 3 classes that were taught the most per room.
        # @Alanis
        # return ClassDAO().get_top_classes_in_room()
        pass

    # Global Statistics ---------------------------------------------+
    def topMeetingsSemester(self):
        # TODO Top 5 meetings with the most sections.
        # @Alanis
        # return MeetingDAO().get_top_meetings()
        pass

    def top_pre_requisite(self):
        dao = ClassDAO()
        result = []
        temp = dao.get_top_prerequisites()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['count'] = tuple[0]
                tempdict['requid'] = tuple[1]
                tempdict['cdesc'] = tuple[2]
                result.append(tempdict)
        else:
            return jsonify("Error not executed"),404

        return jsonify(result)

    def top_least_classes(self):
        dao = ClassDAO()
        result = []
        temp = dao.get_least_classes()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['cid'] = tuple[0]
                tempdict['count'] = tuple[1]
                tempdict['cdesc'] = tuple[2]
                result.append(tempdict)
        else:
            return jsonify("Error not executed"),404

        return jsonify(result)

    def totat_sections(self):
        dao = SectionDAO()
        result = []
        temp = dao.get_sections_per_year()
        if temp:
            for tuple in temp:
                tempdict = {}
                tempdict['year'] = tuple[0]
                tempdict['total_sections'] = tuple[1]
                result.append(tempdict)
        else:
            return jsonify("Error not executed"),404

        return jsonify(result)