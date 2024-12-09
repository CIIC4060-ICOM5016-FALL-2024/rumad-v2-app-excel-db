from dal.requisite_dao import RequisiteDAO
from flask import jsonify

attributes = ["classid", "reqid", "prereq"]


class RequisiteModel:

    def __init__(self):
        pass

    @staticmethod
    def jsonify_response(response, classid = None, reqid = None):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return (
                jsonify(
                    {f"Error":"The requested requisite with ID {reqid} with class ID {classid} was not found."}
                ),
                404,
            )

        result = []

        for req in response:
            result_dict = {
                "classid": req[0],
                "reqid": req[1],
                "prereq": req[2],
            }
            result.append(result_dict)

        return jsonify(result), 200

    @staticmethod
    def post_requisite(data):
        """
        Creates a new requisite tuple in the requisite relation database.
        @param data: a list with requisite attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            req_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f"Missing required attribute: {missing_attribute}"), 400

        classid = req_attributes["classid"]
        reqid = req_attributes["reqid"]
        prereq = req_attributes["prereq"]

        dao = RequisiteDAO()

        response = dao.post_requisite(classid, reqid, prereq)

        if False in response:
            return (
                jsonify(
                    f"Could not create requisite ({classid},{reqid}). Reason: {response[1]} - {response[2]}"
                ),
                400,
            )

        return (
            jsonify(
                f"Requisite (class id:{classid},req id:{reqid}) created successfully"
            ),
            201,
        )

    def get_all_requisites(self):
        """
        Gets all requisite from the requisite relation database.
        @return: JSON and HTTP response code
        """
        dao = RequisiteDAO()
        response = dao.get_all_requisites()
        return self.jsonify_response(response)

    def get_requisite_by_id(self, classid, reqid):
        """
        Gets a requisite from the requisite relation database.
        @param classid: class id
        @param reqid: requisite id
        @return: JSON and HTTP response code
        """
        dao = RequisiteDAO()
        response = dao.get_requisite_by_reqid(int(classid), int(reqid))
        return self.jsonify_response(response, classid, reqid)

    @staticmethod
    def put_requisite_by_classid_reqid(classid, reqid, data):
        """
        Updates a requisite from the requisite relation database.
        @param classid: class id
        @param reqid: requisite id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = RequisiteDAO()
        response = dao.put_requisite_by_classid_reqid(classid, reqid, data)

        if False in response:
            if False in dao.get_requisite_by_reqid(int(classid),int(reqid)):
                return (
                    jsonify(
                        f"Could not update requiste with ID {reqid} with class ID{classid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not update requiste with ID {reqid} with class ID{classid}."
                    ),
                    400,
                )

        return (
            jsonify(
                f"Requisite (class id:{classid},req id:{reqid}) updated successfully"
            ),
            200,
        )

    @staticmethod
    def delete_requisite(classid, reqid):
        """
        Deletes a requisite from the requisite relation database.
        @param classid: class id
        @param reqid: requisite id
        @return: JSON and HTTP response code
        """
        dao = RequisiteDAO()
        response = dao.delete_requisite(int(classid), int(reqid))

        if False in response:
            if False in dao.get_requisite_by_reqid(int(classid),int(reqid)):
                return (
                    jsonify(
                        f"Could not delete requiste with ID {reqid} with class ID {classid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not delete requiste with ID {reqid} with class ID {classid}."
                    ),
                    400,
                )

        return (
            jsonify(
                f"Requisite (class id:{classid},req id:{reqid}) deleted successfully"
            ),
            200,
        )
