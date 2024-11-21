from model.requisite_dao import RequisiteDAO
from flask import jsonify

class Requisite_Controller:

    def __init__(self):
        pass

    def result_requisite(requisites):
        result = []
        if requisites:
            for item in requisites:
                result_dict = {
                    "classid": item[0],
                    "reqid": item[1],
                    "prereq": item[2],
                }
                result.append(result_dict)
            return jsonify(result)
        return jsonify("Error not executed"), 404

    def post_requisite(self, data):
        dao = RequisiteDAO()
        classid = data["classid"]
        reqid = data["reqid"]
        prereq = data["prereq"]
        if dao.post_requisite(classid, reqid, prereq):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_requisites(self):
        dao = RequisiteDAO()
        requisites = dao.get_all_requisites()
        return self.result_requisite(requisites)

    def get_requisite_by_id(self, cid, reqid):
        dao = RequisiteDAO()
        requisites = dao.get_requisite_by_reqid(int(cid), reqid)
        return self.result_requisite(requisites)

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