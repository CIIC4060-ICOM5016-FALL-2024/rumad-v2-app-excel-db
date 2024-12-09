from dal.meeting_dao import MeetingDAO
from flask import jsonify

attributes = ["ccode", "starttime", "endtime", "cdays"]

class MeetingModel:

    def __init__(self):
        pass

    @staticmethod
    def jsonify_response(response, mid = None):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return (
                jsonify(f"The requested meeting with ID {mid} was not found."),
                404,
            )  # not found

        result = []
        for meet in response:
            result_dict = {
                "mid": meet[0],
                "ccode": meet[1],
                "starttime": meet[2],
                "endtime": meet[3],
                "cdays": meet[4],
            }
            result.append(result_dict)

        return jsonify(result)

    def get_all_meetings(self):
        """
        Get all meetings from the meeting relation database.
        @return: JSON and HTTP response code
        """
        dao = MeetingDAO()
        response = dao.get_all_meetings()
        return self.jsonify_response(response)

    @staticmethod
    def post_meeting(data):
        """
        Create a new meeting tuple in the meeting relation database.
        @param data: a list with meeting attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            meeting_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f"Missing required attribute: {missing_attribute}"), 400

        ccode = meeting_attributes["ccode"]
        starttime = meeting_attributes["starttime"]
        endtime = meeting_attributes["endtime"]
        cdays = meeting_attributes["cdays"]

        dao = MeetingDAO()
        response = dao.post_meeting(ccode, starttime, endtime, cdays)

        if False in response:
            return jsonify(f"Could not create meeting for course {ccode}."), 400

        return jsonify(f"Meeting has been created with mid: {response[1]}"), 201

    def get_meeting_by_id(self, mid):
        """
        Get a meeting by id from the meeting relation database.
        @param mid: meeting id
        @return: JSON and HTTP response code
        """
        dao = MeetingDAO()
        response = dao.get_meeting_by_mid(int(mid))
        return self.jsonify_response(response,mid)

    @staticmethod
    def put_meeting_by_id(mid, data):
        """
        Update a meeting by id from the meeting relation database.
        @param mid: meeting id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = MeetingDAO()
        response = dao.put_meeting_by_mid(int(mid), data)
        if False in response:
            if False in dao.get_meeting_by_mid(int(mid)):
                return (
                    jsonify(
                        f"Could not update meeting with ID {mid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not update meeting with ID {mid}."
                    ),
                    400,
                )
        return jsonify(f"Meeting {mid} has been updated"), 200

    @staticmethod
    def delete_meeting(mid):
        """
        Delete a meeting from the meeting relation database.
        @param mid: meeting id
        @return: JSON and HTTP response code
        """
        dao = MeetingDAO()
        response = dao.delete_meeting(int(mid))
        if False in response:
            if False in dao.get_meeting_by_mid(int(mid)):
                return (
                    jsonify(
                        f"Could not delete meeting with ID {mid}. ID does not exist."
                    ),
                    400,
                )
            return (
                    jsonify(
                        f"Could not delete meeting with ID {mid}."
                    ),
                    400,
                )
        return jsonify(f"Meeting {mid} has been deleted"), 200