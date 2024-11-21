from model.meeting_dao import MeetingDAO
from flask import jsonify

class Meeting_Controller:

    def __init__(self):
        pass

    def result_meeting(meetings):
        result = []
        if meetings:
            for item in meetings:
                result_dict = {
                    "mid": item[0],
                    "starttime": item[1],
                    "endtime": item[2],
                    "cdays": item[3],
                    "section_amount": item[4],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def get_meetings(self):
        dao = MeetingDAO()
        meetings = dao.get_all_meetings()
        return self.result_meeting(meetings)

    def post_meeting(self, data):
        dao = MeetingDAO()
        ccode = data["ccode"]
        starttime = data["starttime"]
        endtime = data["endtime"]
        cdays = data["cdays"]
        if dao.post_meeting(ccode, starttime, endtime, cdays):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_meeting_by_id(self, mid):
        dao = MeetingDAO()
        meeting = dao.get_meeting_by_mid(int(mid))
        return self.result_meeting(meeting)

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