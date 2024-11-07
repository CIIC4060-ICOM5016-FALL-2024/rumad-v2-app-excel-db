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

    def get_requisite_by_cid_reqid(self, classid: int, reqid: int):
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
    def put_requisite_classid(self, classid: int, reqid: int, classid_new: int):
        """
        Updates the classid of a tuple in the requisite relation
        :param reqid: requisite id
        :param classid: class id
        :param classid_new: new class id
        :return: True if success, False otherwise
        """
        query = "UPDATE requisite SET classid = %s WHERE classid = %s AND reqid = %s"
        values = [classid_new, classid, reqid]
        return self.update(query, values)

    def put_requisite_reqid(self, classid: int, reqid: int, reqid_new: int):
        """
        Updates the reqid of a tuple in the requisite relation
        :param classid: class id
        :param reqid: requisite id
        :param reqid_new: new requisite id
        :return: True if success, False otherwise
        """
        query = "UPDATE requisite SET reqid = %s WHERE classid = %s and reqid = %s"
        values = [reqid_new, classid, reqid]
        return self.update(query, values)

    def put_requisite_prereq(self, classid: int, reqid: int, prereq: bool):
        """
        Updates the reqid of a tuple in the requisite relation
        :param classid: class id
        :param reqid: requisite id
        :param prereq: True if pre-requisite, False if co-requisite
        :return: True if success, False otherwise
        """
        query = "UPDATE requisite SET prereq = %s WHERE classid = %s AND reqid = %s"
        value = [prereq, classid, reqid]
        return self.update(query, value)

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
