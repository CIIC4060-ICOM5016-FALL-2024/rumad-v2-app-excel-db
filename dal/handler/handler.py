from dal.dao.class_dao import ClassDAO
from dal.dao.meeting_dao import MeetingDAO
from dal.dao.requisite_dao import RequisiteDAO
from dal.dao.room_dao import RoomDAO
from dal.dao.section_dao import SectionDAO

from flask import jsonify


class Handler:
    def __init__(self):
        pass

    # Class Handlers -----------------+
    def post_class(self, data):
        dao = ClassDAO()
        cid = data["cid"]
        cname = data["cname"]
        ccode = data["ccode"]
        cdesc = data["cdesc"]
        term = data["term"]
        years = data["years"]
        cred = data["cred"]
        csyllabus = data["csyllabus"]
        if dao.post_class(cid, cname, ccode, cdesc, term, years, cred, csyllabus):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_classes(self):
        result = []
        dao = ClassDAO()
        classes = dao.get_all_classes()
        if classes:
            for item in classes:
                result_dict = {
                    "cid": item[0],
                    "cname": item[1],
                    "ccode": item[2],
                    "cdesc": item[3],
                    "term": item[4],
                    "years": item[5],
                    "cred": item[6],
                    "csyllabus": item[7],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def get_class_by_id(self, cid):
        result = []
        dao = ClassDAO()
        classes = dao.get_class_by_cid(int(cid))
        if classes:
            for item in classes:
                resultDict = {
                    "cid": item[0],
                    "cname": item[1],
                    "ccode": item[2],
                    "cdesc": item[3],
                    "term": item[4],
                    "years": item[5],
                    "cred": item[6],
                    "csyllabus": item[7],
                }
                result.append(resultDict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def put_class_by_id(self, cid, data):
        dao = ClassDAO()
        if dao.put_class_by_cid(int(cid), data):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def delete_class_by_id(self, cid):
        dao = ClassDAO()
        if dao.delete_class_by_id(int(cid)):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    # REQUISITE HANDLER ----------------+
    def post_requisite(self, data):
        dao = RequisiteDAO()
        classid = data["classid"]
        reqid = data["reqid"]
        prereq = data["prereq"]
        if dao.post_requisite(classid, reqid, prereq):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_requisites(self):
        result = []
        dao = RequisiteDAO()
        requisites = dao.get_all_requisites()
        if requisites:
            for item in requisites:
                result_dict = {"classid": item[0], "reqid": item[1], "prereq": item[2]}
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def get_requisite_by_id(self, cid, reqid):
        result = []
        dao = RequisiteDAO()
        requisites = dao.get_requisite_by_reqid(int(cid), reqid)
        if requisites:
            for item in requisites:
                result_dict = {"classid": item[0], "reqid": item[1], "prereq": item[2]}
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def put_requisite_by_classid_reqid(self, classid, reqid, data):
        dao = RequisiteDAO()
        if dao.put_requisite_by_classid_reqid(classid, reqid, data):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def delete_requisite(self, classid, reqid):
        dao = RequisiteDAO()
        if dao.delete_requisite(classid, reqid):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    # SECTIONS Handlers -----------------+
    def get_sections(self):
        result = []
        dao = SectionDAO()
        sections = dao.get_all_sections()
        if sections:
            for item in sections:
                result_dict = {
                    "sid": item[0],
                    "roomid": item[1],
                    "cid": item[2],
                    "mid": item[3],
                    "semester": item[4],
                    "years": item[5],
                    "capacity": item[6],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def post_section(self, data):
        dao = SectionDAO()
        sid = data["sid"]
        roomid = data["roomid"]
        cid = data["cid"]
        mid = data["mid"]
        semester = data["semester"]
        years = data["years"]
        capacity = data["capacity"]
        if dao.post_section(sid, roomid, cid, mid, semester, years, capacity):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_section_by_id(self, sid):
        result = []
        dao = SectionDAO()
        section = dao.get_section_by_sid(int(sid))
        if section:
            for item in section:
                result_dict = {
                    "sid": item[0],
                    "roomid": item[1],
                    "cid": item[2],
                    "mid": item[3],
                    "semester": item[4],
                    "years": item[5],
                    "capacity": item[6],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def put_section_by_id(self, sid, data):
        dao = SectionDAO()
        if dao.put_section_by_sid(int(sid), data):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def delete_section(self, sid):
        dao = SectionDAO()
        if dao.delete_section(int(sid)):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    # MEETINGS Handlers -----------------+
    def get_meetings(self):
        result = []
        dao = MeetingDAO()
        meetings = dao.get_all_meetings()
        if meetings:
            for item in meetings:
                result_dict = {
                    "mid": item[0],
                    "ccode": item[1],
                    "starttime": item[2],
                    "endtime": item[3],
                    "cdays": item[4],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def post_meeting(self, data):
        dao = MeetingDAO()
        mid = data["mid"]
        ccode = data["ccode"]
        starttime = data["starttime"]
        endtime = data["endtime"]
        cdays = data["cdays"]
        if dao.post_meeting(mid, ccode, starttime, endtime, cdays):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_meeting_by_id(self, mid):
        result = []
        dao = MeetingDAO()
        meeting = dao.get_meeting_by_mid(int(mid))
        if meeting:
            for item in meeting:
                result_dict = {
                    "mid": item[0],
                    "ccode": item[1],
                    "starttime": item[2],
                    "endtime": item[3],
                    "cdays": item[4],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def put_meeting_by_id(self, mid, data):
        dao = MeetingDAO()
        if dao.put_meeting_by_mid(int(mid), data):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def delete_meeting(self, mid):
        dao = MeetingDAO()
        if dao.delete_meeting(int(mid)):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    # ROOM Handlers -----------------+
    def get_rooms(self):
        result = []
        dao = RoomDAO()
        rooms = dao.get_all_rooms()
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

    def post_rooms(self, data):
        dao = RoomDAO()
        rid = data["rid"]
        building = data["building"]
        room_number = data["room_number"]
        capacity = data["capacity"]
        if dao.post_room(rid, building, room_number, capacity):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_room_by_id(self, rid):
        result = []
        dao = RoomDAO()
        room = dao.get_room_by_rid(rid)
        if room:
            for item in room:
                result_dict = {
                    "rid": item[0],
                    "building": item[1],
                    "room_number": item[2],
                    "capacity": item[3]
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

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

    # LOCAL STATISTICS -----------------+
    def top_room_capacity_by_building(self, building):
        result = []
        dao = RoomDAO()
        rooms = dao.get_top_rooms_in_building(building)
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

    def top_ratio_rooms(self, id):
        result = []
        dao = RoomDAO()
        rooms = dao.get_top_ratio_rooms(id)
        if rooms:
            for item in rooms:
                result_dict = {
                    "rid": item[0],
                    "building": item[1],
                    "room_number": item[2],
                    "capacity": item[3],
                }
                result.append(result_dict)
        else:
            return jsonify("Error not executed"), 404
        return jsonify(result)

    def top_classes_per_room(self, id):
        result = []
        dao = ClassDAO()
        classes = dao.get_top_classes_per_room(id)
        if classes:
            for item in classes:
                result_dict = {
                    "cid": item[0],
                    "cname": item[1],
                    "ccode": item[2],
                    "cdesc": item[3],
                    "term": item[4],
                    "years": item[5],
                    "cred": item[6],
                    "csyllabus": item[7],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def top_classes_per_semester(self, year, semester):
        result = []
        dao = ClassDAO()
        classes = dao.get_top_classes_per_year(year, semester)
        if classes:
            for item in classes:
                result_dict = {
                    "cid": item[0],
                    "cname": item[1],
                    "ccode": item[2],
                    "cdesc": item[3],
                    "term": item[4],
                    "years": item[5],
                    "cred": item[6],
                    "csyllabus": item[7],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    # GLOBAL STATISTICS -----------------+
    def top_meeting(self):
        result = []
        dao = MeetingDAO()
        meetings = dao.get_top_meetings()
        if meetings:
            for item in meetings:
                result_dict = {
                    "mid": item[0],
                    "ccode": item[1],
                    "starttime": item[2],
                    "endtime": item[3],
                    "cdays": item[4],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

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
