from dal.dao.dao import DAO
from psycopg2 import sql


class RequisiteDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_requisite(self, classid: int, reqid: int, prereq: bool):
        """
        Creates a tuple in the requisite relation
        :param classid: class id
        :param reqid: requisite id
        :param prereq: True if pre-requisite, False if co-requisite
        :return: True if success, False otherwise
        """
        query = "INSERT INTO requisite (classid, reqid, prereq) VALUES (%s, %s, %s)"
        values = [classid, reqid, prereq]
        return self.create(query, values)

    # GET
    def get_all_requisites(self):
        """
        Gets all tuples from the requisite relation
        :return: A list of tuples, None otherwise
        """
        query = "SELECT * FROM requisite"
        return self.read(query)

    def get_requisite_by_reqid(self, classid: int, reqid: int):
        """
        Gets a tuple from the requisite relation
        :param classid: class id
        :param reqid: requisite id
        :return: A list with a single tuple, None otherwise
        """
        query = "SELECT * FROM requisite WHERE classid = %s AND reqid = %s"
        values = [classid, reqid]
        return self.read(query, values)

    # PUT
    def put_requisite_by_classid_reqid(self, classid: int, reqid: int, data):
        """
        Updates the classid of a tuple in the requisite relation
        :param reqid: requisite id
        :param classid: class id
        :param data: new data
        :return: True if success, False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        params = tuple(data.values()) + (classid, reqid, )
        query = f"UPDATE requisite SET {new} WHERE classid = %s AND reqid = %s"
        values = [params]
        return self.update(query, values)

    # DELETE
    def delete_requisite(self, classid: int, reqid: int):
        """
        Deletes a tuple from the requisite relation
        :param classid: class id
        :param reqid: requisite id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM requisite WHERE classid = %s AND reqid = %s"
        values = [classid, reqid]
        return self.delete(query, values)
