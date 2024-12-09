from dal.section_dao import SectionDAO
from flask import jsonify

attributes = ["roomid", "cid", "mid", "semester", "years", "capacity"]

class SectionModel:

    def __init__(self):
        pass

    @staticmethod  # It runs the same in any instance of the class
    def jsonify_response(response, sid = None):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return (
                jsonify(f"The requested section with ID {sid} was not found."),
                404,
            )  # Not found

        result = []
        for section in response:
            result_dict = {
                "sid": section[0],
                "roomid": section[1],
                "cid": section[2],
                "mid": section[3],
                "semester": section[4],
                "years": section[5],
                "capacity": section[6],
            }
            result.append(result_dict)
        return jsonify(result), 200

    def get_all_sections(self):
        """
        Gets all sections from the section relation database.
        @return: JSON and HTTP response code
        """
        dao = SectionDAO()
        response = dao.get_all_sections()
        return self.jsonify_response(response)

    @staticmethod
    def post_section(data):
        """
        Creates a new section tuple in the section relation database.
        @param data: list with section attributes to be added
        @return: JSON and HTTP response code
        """

        # Check that all attributes are present
        try:
            section_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f"Missing required attribute: {missing_attribute}"), 400

        dao = SectionDAO()

        roomid = section_attributes["roomid"]
        cid = section_attributes["cid"]
        mid = section_attributes["mid"]
        semester = section_attributes["semester"]
        years = section_attributes["years"]
        capacity = section_attributes["capacity"]

        response = dao.post_section(roomid, cid, mid, semester, years, capacity)

        if False in response:
            return jsonify(f"Could not create section (sid: {response[1]})."), 400
        return jsonify(f"Section (sid: {response[1]}) successfully created"), 201

    def get_section_by_id(self, sid):
        """
        Gets a specified section from the section relation database.
        @param sid: section id
        @return: JSON and HTTP response code
        """
        dao = SectionDAO()
        response = dao.get_section_by_sid(int(sid))
        return self.jsonify_response(response, sid)

    @staticmethod
    def put_section_by_id(sid, data):
        """
        Updates a specified section from the section relation database.
        @param sid: section id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = SectionDAO()
        response = dao.put_section_by_sid(int(sid), data)

        if False in response:
            if False in dao.get_section_by_sid(int(sid)):
                return (
                    jsonify(
                        f"Could not update section with ID {sid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not update section with ID {sid}."
                    ),
                    400,
                )

        if False in response:
            return jsonify(f"Failed to update section with ID {sid}."), 400
        return jsonify(f"Section with sid {sid} successfully updated"), 200

    @staticmethod
    def delete_section(sid):
        """
        Deletes a specified section from the section relation database.
        @param sid: section id
        @return: JSON and HTTP response code
        """
        dao = SectionDAO()
        response = dao.delete_section(int(sid))

        if False in response:
            if False in dao.get_section_by_sid(int(sid)):
                return (
                    jsonify(
                        f"Could not delete section with ID {sid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not delete section with ID {sid}."
                    ),
                    400,
                )
        return jsonify(f"Section with sid {sid} deleted: {response[1]}"), 200