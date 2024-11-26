
from dal.section_dao import SectionDAO
from dal.class_dao import ClassDAO
from dal.meeting_dao import MeetingDAO
from dal.room_dao import RoomDAO


from flask import jsonify

class StatisticsModel:

    def __init__(self):
        pass

    """ LOCAL STATISTICS """
    @staticmethod
    def top_room_capacity_by_building(building):
        """
        Gets top 3 rooms with the most capacity in a building
        @param building: name of building
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.get_top_rooms_in_building(building)
        result = []
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500  # Internal Server Error
        for item in response:
            result_dict = {
                "rid": item[0],
                "building": item[1],
                "room_number": item[2],
                "capacity": item[3]
            }
            result.append(result_dict)
        return jsonify(result), 200

    @staticmethod
    def top_ratio_rooms(building):
        """
        Gets top 3 rooms with the most student to capacity ratio in a building
        @param building: name of building
        @return: JSON and HTTP response code
        """
        dao = RoomDAO()
        response = dao.get_top_ratio_rooms(building)

        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        result = []

        for item in response:
            result_dict = {
                "rid": item[0],
                "building": item[1],
                "room_number": item[2],
                "capacity": item[3],
                "ratio": item[4]
            }
            result.append(result_dict)
        return jsonify(result), 200


    @staticmethod
    def top_classes_per_room(rid):
        """
        Gets top 3 classes taught the most in room specified
        @param rid: room id
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()
        response = dao.get_top_classes_per_room(rid)
        result = []
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500
        for item in response:
            result_dict = {
                "cid" : item[0],
                "cname" : item[1],
                "ccode" : item[2],
                "cdesc" : item[3],
                "term" : item[4],
                "years" : item[5],
                "cred" : item[6],
                "csyllabus" : item[7],
                "amount" : item[8]
            }
            result.append(result_dict)
        return jsonify(result), 200

    @staticmethod
    def top_classes_per_semester(year, semester):
        """
        Gets top 3 classes taught the most in a semester and year
        @param year: integer year
        @param semester:  semester
        @return:
        """
        dao = ClassDAO()
        response = dao.get_top_classes_per_year(year, semester)
        result = []
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500
        for item in response:
            result_dict = {
                "cid" : item[0],
                "cname" : item[1],
                "ccode" : item[2],
                "cdesc" : item[3],
                "term" : item[4],
                "years" : item[5],
                "cred" : item[6],
                "csyllabus": item[7],
                "section_amount" : item[8],
            }
            result.append(result_dict)
        return jsonify(result), 200

    """ GLOBAL STATISTICS """
    @staticmethod
    def top_meeting():
        """
        Gets the top 5 meetings with the most sections.
        @return: JSON and HTTP response code
        """
        dao = MeetingDAO()
        response = dao.get_top_meetings()

        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        result = []

        for item in response:
            result_dict = {
                "mid" : item[0],
                "ccode": item[1],
                "starttime" : item[2],
                "endtime" : item[3],
                "cdays" : item[4],
                "frequency" : item[5]
            }
            result.append(result_dict)
        return jsonify(result), 200

    @staticmethod
    def top_pre_requisite():
        """
        Gets the top 3 classes that appear the most as prerequisite to other classes
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()

        response = dao.get_top_prerequisites()


        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        result = []

        for item in response:
            result_dict = {"cid" : item[0], "cname": item[1], "ccode": item[2], "cdesc": item[3],
                           "term": item[4], "years": item[5], "cred": item[6], "csyllabus": item[7],
                           "frequency": item[8]}
            result.append(result_dict)
        return jsonify(result), 200


    @staticmethod
    def top_least_classes():
        """
        Get the top 3 classes that are offered the least
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()
        response = dao.get_least_classes()

        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        result = []

        for item in response:
            result_dict = {"cid": item[0], "cname": item[1], "ccode": item[2], "cdesc": item[3],
                           "term": item[4], "years": item[5], "cred": item[6], "csyllabus": item[7],
                           "frequency": item[8]}
            result.append(result_dict)
        return jsonify(result), 200

    @staticmethod
    def total_sections():
        """
        Gets the total number of sections per year
        @return: JSON and HTTP response code
        """
        dao = SectionDAO()
        response = dao.get_sections_per_year()
        result = []
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        for item in response:
            result_dict = { "year" : item[0], "total_sections" : item[1] }
            result.append(result_dict)

        return jsonify(result), 200


