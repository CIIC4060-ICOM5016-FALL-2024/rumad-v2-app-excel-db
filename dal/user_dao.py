from dal.dao import DAO

class UserDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_user(self, username, email, password):
        """
        Creates a new user in the database
        @param username: account username
        @param email: account email
        @param password: account password
        @return: A tuple with True and the userid if successful,
        a tuple with False and error message if unsuccessful
        """
        query = "INSERT INTO public.user (username, email, password) VALUES (%s, %s, %s) RETURNING uid"
        values = [username, email, password]
        return self.create(query, values)

    def get_user_by_id(self, uid: int):
        """
        Gets a tuple from the user relation
        @param uid: user id
        @return: a list with a single tuple or tuple with False and error messages
        """
        query = "SELECT * FROM public.user WHERE uid = %s"
        value = [uid]
        return self.read(query, value)

    def get_user_by_username(self, username: str):
        """
        Gets a tuple from the user relation
        @param username: account username
        @return:a list with a single tuple or tuple with False and error messages
        """
        query = "SELECT * FROM public.user WHERE username = %s"
        value = [username]
        return self.read(query, value)

    def get_user_by_email(self, email: str):
        """
        Gets a tuple from the user relation
        @param email: account email
        @return: a list with a single tuple or tuple with False and error messages
        """
        query = "SELECT * FROM public.user WHERE email = %s"
        value = [email]
        return self.read(query, value)

    # PUT
    def put_user_by_id(self, uid: int, data):
        """
        Updates a tuple in the user relation
        @param uid: user id
        @param data: attributes to be updated
        @return: a tuple with True if success, a tuple False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (uid,)
        query = f"UPDATE public.user SET {new} WHERE uid = %s"
        return self.update(query, values)

    def put_user_by_username(self, username: str, data):
        """
        Updates a tuple in the user relation
        @param username: account username
        @param data: attributes to be updated
        @return: a tuple with True if success, a tuple with False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (username,)
        query = f"UPDATE public.user SET {new} WHERE username = %s"
        return self.update(query, values)

    def put_user_by_email(self, email: str, data):
        """
        Updates a tuple in the user relation
        @param email: account email
        @param data: attributes to be updated
        @return: a tuple with True if success, a tuple with False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (email,)
        query = f"UPDATE public.user SET {new} WHERE email = %s"
        return self.update(query, values)

    # DELETE
    def delete_user_by_id(self, uid: int):
        """
        Deletes a tuple in the user relation
        @param uid: user id
        @return: a tuple with True if success, a tuple with False otherwise
        """
        query = "DELETE FROM public.user WHERE uid = %s"
        values = [uid]
        return self.delete(query, values)

    def delete_user_by_username(self, username: str):
        """
        Deletes a tuple in the user relation
        @param username: account username
        @return: a tuple with True if success, a tuple with False otherwise
        """
        query = "DELETE FROM public.user WHERE username = %s"
        values = [username]
        return self.delete(query, values)

    def delete_user_by_email(self, email: str):
        """
        Deletes a tuple in the user relation
        @param email: account email
        @return: a tuple with True if success, a tuple with False otherwise
        """
        query = "DELETE FROM public.user WHERE email = %s"
        values = [email]
        return self.delete(query, values)


