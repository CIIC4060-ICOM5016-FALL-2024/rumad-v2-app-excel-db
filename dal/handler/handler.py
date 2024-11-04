from dal.dao.class_dao import ClassDAO
from dal.dao.section_dao import SectionDAO
from flask import jsonify

class Handler:
    def __init__(self):
        print("I handle errors and jsonfy results")

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
            return "Error not executed",404

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
            return "Error not executed",404

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
            return "Error not executed",404

        return jsonify(result)