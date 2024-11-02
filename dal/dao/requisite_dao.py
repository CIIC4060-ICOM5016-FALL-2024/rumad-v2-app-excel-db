from dao import DAO
from psycopg import sql


class RequisiteDAO(DAO):
    relation = 'requisite'

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
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s)")
                 .format(sql.Identifier(self.relation)))
        values = [classid, reqid, prereq]
        return self.create(query, values)

    # GET
    def get_all_requisites(self):
        """
        Gets all tuples from the requisite relation
        :return: A list of tuples, None otherwise
        """
        query = (sql.SQL("SELECT * FROM {}")
                 .format(sql.Identifier(self.relation)))
        return self.read(query)

    def get_requisite_by_reqid(self, reqid: int):
        """
        Gets a tuple from the requisite relation
        :param reqid: requisite id
        :return: A list with a single tuple, None otherwise
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('reqid'), reqid))
        return self.read(query)

    # PUT
    def put_requisite_reqid(self, reqid: int, reqid_new: int):
        """
        Updates the reqid of a tuple in the requisite relation
        :param reqid: requisite id
        :param reqid_new: new requisite id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('reqid'), reqid_new,
                         sql.Identifier('reqid'), reqid))
        return self.update(query)

    def put_requisite_classid(self, reqid: int, classid: int):
        """
        Updates the classid of a tuple in the requisite relation
        :param reqid: requisite id
        :param classid: class id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('classid'), classid,
                         sql.Identifier('reqid'), reqid))
        return self.update(query)

    def put_requisite_prereq(self, reqid: int, prereq: bool):
        """
        Updates the reqid of a tuple in the requisite relation
        :param reqid: requisite id
        :param prereq: True if pre-requisite, False if co-requisite
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('prereq'), prereq,
                         sql.Identifier('reqid'), reqid))
        return self.update(query)

    # DELETE
    def delete_requisite(self, reqid: int):
        """
        Deletes a tuple from the requisite relation
        :param reqid: requisite id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('reqid'), reqid))
        return self.delete(query)
