from dal.dao.dao import DAO

class UserDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_user(self, username, email, hashed_password):
        query = "INSERT INTO user (username, email, password) VALUES (%s, %s, %s)"
        values = [username, email, hashed_password]
        return self.create(query, values)

    # GET
    def get_all_users(self):
        """
        Retrieve all users, excluding passwords.
        """
        query = "SELECT uid, username, email FROM user" 
        result = self.read(query)
        return result if result else []

    def get_user_by_uid(self, uid: int):
        query = "SELECT uid, username, email FROM user WHERE uid = %s"
        value = [uid]
        result = self.read(query, value)
        return result[0] if result else None

    def get_user_by_name(self, username):
        query = "SELECT uid, username, email, password FROM user WHERE username = %s LIMIT 1"
        value = [username]
        result = self.read(query, value)
        if result:
            return {
                "uid": result[0][0],
                "username": result[0][1],
                "email": result[0][2],
                "password": result[0][3],
            }
        return None
    
    def get_user_by_email(self, email):
        query = "SELECT uid, username, email FROM user WHERE email = %s LIMIT 1"
        value = [email]
        result = self.read(query, value)
        if result:
            return {
                "uid": result[0][0],
                "username": result[0][1],
                "email": result[0][2],
            }
        return None

    # PUT
    def put_user_by_uid(self, uid: int, data):
        if not data:
            raise ValueError("No data provided for update")

        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (uid,)
        query = f"UPDATE user SET {new} WHERE uid = %s"
        return self.update(query, values)

    # DELETE
    def delete_user(self, uid: int):
        query = "DELETE FROM user WHERE uid = %s"
        values = [uid]
        return self.delete(query, values)