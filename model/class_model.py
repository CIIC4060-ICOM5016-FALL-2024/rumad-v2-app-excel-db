from http.client import responses

from dal.class_dao import ClassDAO
from flask import jsonify

attributes = ["cname", "ccode", "cdesc", "term", "years", "cred", "csyllabus"]


class ClassModel:

    def __init__(self):
        pass

    @staticmethod
    def jsonify_response(response):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """

        if False in response:
            return (
                jsonify(
                    f"The requested class with ID {response[1]} was not found. Reason: {response[1]} - {response[2]}"
                ),
                404,
            )  # not found

        result = []

        for course in response:
            result_dict = {
                "cid": course[0],
                "cname": course[1],
                "ccode": course[2],
                "cdesc": course[3],
                "term": course[4],
                "years": course[5],
                "cred": course[6],
                "csyllabus": course[7],
            }
            result.append(result_dict)

        return jsonify(result), 200

    @staticmethod
    def post_class(data):
        """
        Creates a new class tuple in the class relation database.
        @param data: list with class attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            class_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f"Missing required attribute: {missing_attribute}"), 400

        cname = class_attributes["cname"]
        ccode = class_attributes["ccode"]
        cdesc = class_attributes["cdesc"]
        term = class_attributes["term"]
        years = class_attributes["years"]
        cred = class_attributes["cred"]
        csyllabus = class_attributes["csyllabus"]

        dao = ClassDAO()

        response = dao.post_class(cname, ccode, cdesc, term, years, cred, csyllabus)

        if False in response:
            return (
                jsonify(
                    f"Could not create class {cdesc}. Reason: {response[1]} - {response[2]}."
                ),
                400,
            )

        return (
            jsonify(f"Class {cdesc} created successfully with cid: {response[1]}"),
            201,
        )

    def get_all_classes(self):
        """
        Gets all classes from the section relation database.
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()
        response = dao.get_all_classes()
        return self.jsonify_response(response)

    def get_class_by_id(self, cid):
        """
        Gets a single class by its cid.
        @param cid: class id
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()
        response = dao.get_class_by_cid(int(cid))
        return self.jsonify_response(response)

    @staticmethod
    def put_class_by_id(cid, data):
        """
        Updates a single class by its cid in the class relation database.
        @param cid: class id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = ClassDAO()
        response = dao.put_class_by_cid(int(cid), data)

        if False in response:
            return (
                jsonify(
                    f"Failed to update class {cid}. Reason: {response[1]} - {response[2]}."
                ),
                400,
            )

        return jsonify(f"Class {cid}: updated successfully"), 200

    @staticmethod
    def delete_class_by_id(cid):
        """
        Deletes a single class by its cid in the class relation database.
        @param cid: class id
        @return:
        """
        dao = ClassDAO()
        response = dao.delete_class_by_id(int(cid))

        if False in response:
            return (
                jsonify(
                    f"Could not delete class with ID {cid}. Reason: {response[1]} - {response[2]}."
                ),
                400,
            )
        return jsonify(f"Class {cid} deleted successfully"), 200
