from dal.dao.dao import DAO

class UserDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_user(self, username, email, password):
        query = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
        values = [username, email, password]
        return self.create(query, values)

    # GET
    def get_all_users(self):
        query = "SELECT * FROM users"
        return self.read(query)

    def get_user_by_uid(self, uid: int):
        query = "SELECT * FROM users WHERE uid = %s"
        value = [uid]
        return self.read(query, value)

    def get_user_by_name(self, username: str):
        query = "SELECT * FROM users WHERE username = %s"
        value = [username]
        return self.read(query, value)

    # PUT
    def put_user_by_uid(self, uid: int, data):
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (uid,)
        query = f"UPDATE users SET {new} WHERE uid = %s"
        return self.update(query, values)

    # DELETE
    def delete_user(self, uid: int):
        query = "DELETE FROM users WHERE uid = %s"
        values = [uid]
        return self.delete(query, values)