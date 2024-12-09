import psycopg2
from dal.user_dao import UserDAO
import re
import bcrypt
from flask import jsonify

attributes = ["username", "email", "password"]


class UserModel:
    def __int__(self):
        pass

    @staticmethod
    def jsonify_response(response):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 404  # not found

        result = []
        for user in response:
            result_dict = {
                "uid": user[0],
                "username": user[1],
                "email": user[2],
                "password": user[3]
            }
            result.append(result_dict)
        return jsonify(result), 200

    @staticmethod
    def is_valid_password(password: str):
        """
        Checks if a password is valid.
        @param password: password
        @return: True if password is valid, False otherwise
        """
        if len(password) < 8 or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) or not re.search(r'\d', password):
            return False
        return True

    @staticmethod
    def is_valid_email(email: str):
        """
        Checks if email is valid and from the @upr.edu domain
        @param email: email to check
        @return: True if email is valid, False otherwise
        """
        if not re.match(r'^[a-z]+\.[a-z]+[0-9]*@upr\.edu$', email):
            return False
        return True

    def post_user(self, data):
        """
        Creates a new user tuple in the user relation database.
        @param data: list with user attributes to be added
        @return: JSON and HTTP response code
        """
        try:
            user_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  #bad request
            missing_attribute = e.args[0]
            return jsonify(f'Missing required attribute: {missing_attribute}'), 400

        username = user_attributes["username"]
        email = user_attributes["email"]
        password = user_attributes["password"]

        if not self.is_valid_email(email):
            return {"error": "Invalid email format. Must follow: firstname.lastname@upr.edu"}, 400

        if not self.is_valid_password(password):
            return {"error": "Password does not meet the requirements:\n"
                    "- At least 8 characters in length\n"
                    "- Must contain at least 3 of the following 4 types of characters:\n"
                    "- Lowercase letters (a-z)\n"
                    "- Uppercase letters (A-Z)\n"
                    "- Numbers (i.e. 0-9)\n"
                    "- Special characters (e.g. !@#$%^&*)"}, 400

        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        dao = UserDAO()

        response = dao.post_user(username, email, hashed_password)

        if False in response:
            return {"error": response[2]}, 400

        return jsonify(f'User (uid: {response[1]}) successfully created'), 201

    def get_all_user(self):
        """
        Gets all users from the user relation database.
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.get_all_user()
        result = []
        for user in response:
            resultdict = {}
            resultdict['uid'] = user[0]
            resultdict['username'] = user[1]
            resultdict['email'] = user[2]
            resultdict['password'] = user[3]
            result.append(resultdict)

        return jsonify(result), 200

    def get_user_by_id(self, uid: int):
        """
        Retrieves a user by uid.
        @param uid: user id
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.get_user_by_id(uid)
        return self.jsonify_response(response)

    def get_user_by_username(self, username: str):
        """
        Retrieves a user by username.
        @param username: username
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.get_user_by_username(username)
        return self.jsonify_response(response)

    def get_user_by_email(self, email: str):
        """
        Retrieves a user by email.
        @param email: user email
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.get_user_by_email(email)
        return self.jsonify_response(response)

    @staticmethod
    def put_user_by_id(uid: int, data: dict):
        """
        Updates a user by uid.
        @param uid: user id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.put_user_by_id(uid, data)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User with uid {uid} successfully updated'), 200

    @staticmethod
    def put_user_by_username(username: str, data: dict):
        """
        Updates a user by username.
        @param username: username
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.put_user_by_username(username, data)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User with username ({username}) successfully updated'), 200

    @staticmethod
    def put_user_by_email(email: str, data: dict):
        """
        Updates a user by email.
        @param email: user email
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.put_user_by_email(email, data)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'Section with email ({email}) successfully updated'), 200

    @staticmethod
    def delete_user_by_id(uid: int):
        """
        Deletes a user by uid.
        @param uid: user id
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.delete_user_by_id(uid)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User with uid {uid} successfully deleted'), 200

    @staticmethod
    def delete_user_by_username(username: str):
        """
        Deletes a user by username.
        @param username: username
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.delete_user_by_username(username)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User with username ({username}) successfully deleted'), 200

    @staticmethod
    def delete_user_by_email(email: str):
        """
        Deletes a user by email.
        @param email: user email
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.delete_user_by_email(email)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 400
        return jsonify(f'User with email ({email}) successfully deleted'), 200

    @staticmethod
    def validate_user_login(data: dict):
        """
        Validates a user login.
        @param data: login data
        @return: JSON and HTTP response code
        """
        try:
            username = data['username']
            password = data['password']
        except KeyError:
            return {"error": "Missing user or password"}, 400

        dao = UserDAO()

        try:
            response = dao.get_user_by_username(username) # Just in case
        except psycopg2.Error as e:
            return {"error": str(e)}, 500

        if False in response:
            return {"error" : "Can't find user"}, 400

        hashed_password = response[0][3]

        # Validate password
        try:
            if bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8')):
                user_data = {
                    "uid": response[0][0],
                    "username": response[0][1],
                    "email": response[0][2]
                }

                return user_data, 200
        except ValueError as e:
            return {"error": str(e)}, 400

        return {"error": "Wrong password"}, 401


