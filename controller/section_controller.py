from model.section_dao import SectionDAO
from flask import jsonify

class Section_Controller:

    def __init__(self):
        pass

    def result_section(sections):
        result = []
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
    
    def get_sections(self):
        dao = SectionDAO()
        sections = dao.get_all_sections()
        return self.result_section(sections)

    def post_section(self, data):
        dao = SectionDAO()
        roomid = data["roomid"]
        cid = data["cid"]
        mid = data["mid"]
        semester = data["semester"]
        years = data["years"]
        capacity = data["capacity"]
        if dao.post_section(roomid, cid, mid, semester, years, capacity):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_section_by_id(self, sid):
        dao = SectionDAO()
        section = dao.get_section_by_sid(int(sid))
        return self.result_section(section)

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