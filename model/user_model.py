from dal.user_dao import UserDAO
from flask import jsonify

attributes = ["uid", "username", "email", "password"]

class UserModel:

    def __init__(self):
        self.dao = UserDAO()

    @staticmethod
    def jsonify_response(response):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 404 # not found

        result = []
        for user in response:
            result_dict = {
                "uid": user[0],
                "username": user[1],
                "email": user[2],
                "password": user[3],
            }
            result.append(result_dict)

        return jsonify(result)

    def get_all_users(self):
        """
        Get all users from the user relation database.
        @return: JSON and HTTP response code
        """
        response = self.dao.get_all_users()
        return self.jsonify_response(response)

    def get_user_by_name(self, username):
        """
        Get a user by its username from the user relation database.
        @param username: User's username
        @return: JSON and HTTP response code
        """
        response = self.dao.get_user_by_name(username)
        return self.jsonify_response(response)

    def post_user(self, data):
        """
        Create a new user tuple in the user relation database.
        @param data: a list with user attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            users_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f'Missing required attribute: {missing_attribute}'), 400

        username = users_attributes["starttime"]
        email = users_attributes["endtime"]
        password = users_attributes["cdays"]

        response = self.dao.post_user(username, email, password)

        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400

        return jsonify(f'User has been created with mid: {response[1]}'), 201

    def get_user_by_id(self, uid):
        """
        Get a user by id from the user relation database.
        @param uid: user id
        @return: JSON and HTTP response code
        """
        response = self.dao.get_user_by_uid(int(uid))
        return self.jsonify_response(response)

    def put_user_by_id(self, uid, data):
        """
        Update a user by id from the user relation database.
        @param uid: user id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        response = self.dao.put_user_by_uid(int(uid), data)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User {uid} has been updated'), 200

    def delete_user(self, uid):
        """
        Delete a user from the user relation database.
        @param uid: user id
        @return: JSON and HTTP response code
        """
        response = self.dao.delete(int(uid))
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User {uid} has been deleted'), 200
