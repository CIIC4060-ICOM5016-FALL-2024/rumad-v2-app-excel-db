from model.class_dao import ClassDAO
from flask import jsonify

class Class_Controller:

    def __init__(self):
        pass

    def result_class(classes):
        result = []
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

    def post_class(self, data):
        dao = ClassDAO()
        cname = data["cname"]
        ccode = data["ccode"]
        cdesc = data["cdesc"]
        term = data["term"]
        years = data["years"]
        cred = data["cred"]
        csyllabus = data["csyllabus"]
        if dao.post_class(cname, ccode, cdesc, term, years, cred, csyllabus):
            return jsonify("Success"), 201
        return jsonify("Error not executed"), 404

    def get_classes(self):
        dao = ClassDAO()
        classes = dao.get_all_classes()
        return self.result_class(classes)

    def get_class_by_id(self, cid):
        dao = ClassDAO()
        classes = dao.get_class_by_cid(int(cid))
        return self.result_class(classes)

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
