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
            return (
                jsonify(f"The requested user with ID {response[1]} was not found."),
                404,
            )  # not found

        result = []
        for user in response:
            result_dict = {
                "uid": user[0],
                "username": user[1],
                "email": user[2],
                "password": user[3],
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
        return len(password) < 8 or not re.search(r'[!@#$%^&*(),.?":{}|<>]', password) or not re.search(r'\d', password)

    @staticmethod
    def is_valid_email(email: str):
        """
        Checks if email is valid and from the @upr.edu domain
        @param email: email to check
        @return: True if email is valid, False otherwise
        """
        return re.match(r'^[a-z]+\.[a-z]+[0-9]*@upr\.edu$', email)
    

    @staticmethod
    def post_user(data):
        """
        Creates a new user tuple in the user relation database.
        @param data: list with user attributes to be added
        @return: JSON and HTTP response code
        """
        try:
            user_attributes = {key: data[key] for key in attributes}
        except KeyError as e:
            missing_attribute = e.args[0]
            return jsonify(f'Missing required attribute: {missing_attribute}'), 400

        valid, processed_data = UserModel.validate_and_process_user_data(user_attributes)
        if not valid:
            return jsonify(processed_data), 400

        dao = UserDAO()
        try:
            response = dao.post_user(processed_data["username"], processed_data["email"], processed_data["password"])
        except psycopg2.IntegrityError:  # Catch duplicate key constraint violations
            return jsonify({"error": "Invalid username or password"}), 400
        except Exception as e:
            return jsonify({"error": "An unexpected error occurred"}), 500

        if False in response:
            return jsonify({"error": response[2]}), 400

        return jsonify(f"User (uid: {response[1]}) successfully created"), 201

    def get_all_user(self):
        """
        Gets all users from the user relation database.
        @return: JSON and HTTP response code
        """
        dao = UserDAO()
        response = dao.get_all_user()
        return jsonify(response), 200

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
        try:
            # Ensure all required attributes are present in the data
            user_attributes = {key: data[key] for key in data.keys()}

            # Validate and process user data
            valid, processed_data = UserModel.validate_and_process_user_data(user_attributes)
            if not valid:
                return jsonify(processed_data), 400
            print(processed_data)
            dao = UserDAO()
            try:
                # Update user in the database
                response = dao.put_user_by_id(uid, processed_data)
            except psycopg2.IntegrityError:  # Handle duplicate key violations
                return jsonify({"error": "Username or email is already taken"}), 400
            except Exception as e:
                return jsonify(f"Unable to update user with ID {uid}."), 400

            if False in response:
                return jsonify({"error": response[2]}), 400

            return jsonify(f"User with uid {uid} successfully updated"), 200

        except KeyError as e:
            missing_attribute = e.args[0]
            return jsonify(f'Missing required attribute: {missing_attribute}'), 400
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return jsonify({"error": "An unexpected error occurred"}), 500

    
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
            return jsonify(f"Unable to update user with username {username}"), 400
        return jsonify(f"User with username ({username}) successfully updated"), 200

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
            return jsonify(f"Unable to update user with email {email}"), 400
        return jsonify(f"Section with email ({email}) successfully updated"), 200

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
            return jsonify(f"Unable to delete the user with uid: {uid}."), 400
        return jsonify(f"User with uid {uid} successfully deleted"), 200

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
            return jsonify(f"Unable to delete the user with username: {username}."), 400
        return jsonify(f"User with username ({username}) successfully deleted"), 200

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
            return jsonify(f"Unable to delete the user with email: {email}."), 400
        return jsonify(f"User with email ({email}) successfully deleted"), 200

    @staticmethod
    def validate_user_login(data: dict):
        """
        Validates a user login.
        @param data: login data
        @return: JSON and HTTP response code
        """
        try:
            username = data["username"]
            password = data["password"]
        except KeyError:
            return {"error": "Missing user or password"}, 400

        dao = UserDAO()

        try:
            response = dao.get_user_by_username(username)  # Just in case
        except psycopg2.Error as e:
            return {"error": str(e)}, 500

        if False in response:
            return {"error": "Can't find user"}, 400

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

    @staticmethod
    def validate_and_process_user_data(data):
        """
        Validates user data (username, email, password), checks if username and email are unique,
        and hashes the password if provided.
        @param data: dictionary containing user attributes
        @param exclude_uid: user ID to exclude from uniqueness checks (used for updates)
        @return: A tuple (True, processed_data) if validation is successful,
                (False, error_message) otherwise.
        """
        username = data.get("username")
        email = data.get("email")
        password = data.get("password")

        dao = UserDAO()
        print(username, email, password)

        # Check if username already exists
        if username:
            existing_user = dao.get_user_by_username(username)
            if not False in existing_user:
                return False, {"error": f"Username is already taken"}

        # Check if email already exists
        if email:
            existing_user = dao.get_user_by_email(email)
            if not False in  existing_user:
                return False, {"error": f"Email is already registered"}

        # Validate email format
        if not UserModel().is_valid_email(email):
            return False, {"error": "Invalid email format. Must follow: firstname.lastname@upr.edu"}

        # Validate and hash password
        if password:
            if UserModel.is_valid_password(password):
                return False, {"error": "Password does not meet the requirements:\n"
                                        "- At least 8 characters in length\n"
                                        "- Must contain at least 3 of the following 4 types of characters:\n"
                                        "- Lowercase letters (a-z)\n"
                                        "- Uppercase letters (A-Z)\n"
                                        "- Numbers (i.e. 0-9)\n"
                                        "- Special characters (e.g. !@#$%^&*)"}
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            data["password"] = hashed_password

        return True, data