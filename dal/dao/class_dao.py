from dao import DAO
from psycopg import sql


class ClassDAO(DAO):
    relation = 'class'

    def __init__(self):
        super().__init__()

    # POST
    def post_class(self, cid: int, cname: str, ccode: int,
                   cdesc: str, term: str, years: str, cred: int, cysllabus: str):
        """
        Creates a tuple in the class relation
        :param cid: class id
        :param cname: class name
        :param ccode: class code
        :param cdesc: class description
        :param term: academic term
        :param years: academic years
        :param cred: credit
        :param cysllabus: class syllabus
        :return: True if success, False otherwise
        """
        query = (sql.SQL("INSERT INTO {} VALUES (%s, %s, %s, %s, %s, %s, %s, %s)")
                 .format(sql.Identifier(self.relation)))
        values = [cid, cname, ccode, cdesc, term, years, cred, cysllabus]
        return self.create(query, values)

    # GET
    def get_all_classes(self):
        """
        Gets all tuples from the class relation
        :return: a list of tuples, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {}")
                 .format(sql.Identifier(self.relation)))
        return self.read(query)

    def get_class_by_cid(self, cid: int):
        """
        Gets a tuple from the class relation
        :param cid: class id
        :return: a list with a single tuple, or None if failed
        """
        query = (sql.SQL("SELECT * FROM {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cid'), cid))
        return self.read(query)

    def get_top_classes(self, year: int, semester: str):
        # TODO Top 3 most taught classes per semester, per year.
        # @Alanis
        return

    def get_top_prerequisites(self):
        # TODO Top 3 classes that appears the most as prerequisite to other classes.
        # @Anthony
        return

    def get_least_classes(self):
        # TODO Top 3 classes that were offered the least
        return

    def get_top_classes_in_room(self, rid: int):
        # TODO Top 3 classes given in a certain room
        return

    # PUT
    def put_class_cid(self, cid: int, cid_new: int):
        """
        Updates the cid of a tuple in the class relation
        :param cid: class id
        :param cid_new: new class id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cid'), cid_new,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_cname(self, cid: int, cname: str):
        """
        Updates the cname of a tuple in the class relation
        :param cid: class id
        :param cname: new class name
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cname'), cname,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_ccode(self, cid: int, ccode: int):
        """
        Updates the ccode of a tuple in the class relation
        :param cid: class id
        :param ccode: new class code
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('ccode'), ccode,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_cdesc(self, cid: int, cdesc: str):
        """
        Updates the cdesc of a tuple in the class relation
        :param cid: class id
        :param cdesc: new class description
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cdesc'), cdesc,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_term(self, cid: int, term: str):
        """
        Updates the term of a tuple in the class relation
        :param cid: class id
        :param term: new academic term
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('term'), term,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_years(self, cid: int, years: str):
        """
        Updates the years of a tuple in the class relation
        :param cid: class id
        :param years: new academic years
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('years'), years,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_cred(self, cid: int, cred: int):
        """
        Updates the creds of a tuple in the class relation
        :param cid: class id
        :param cred: new credits
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('cred'), cred,
                         sql.Identifier('cid'), cid))
        return self.update(query)

    def put_class_csyllabus(self, cid: int, csyllabus: str):
        """
        Updates the csyllabus of a tuple in the class relation
        :param cid: class id
        :param csyllabus: new syllabus
        :return: True if success, False otherwise
        """
        query = (sql.SQL("UPDATE {} SET {} = {} WHERE {} = {}")
                 .format(sql.Identifier(self.relation), sql.Identifier('csyllabus'), csyllabus,
                         sql.Identifier('cid'), cid))
        return self.update(query)


    # DELETE
    def delete_class(self, cid: int):
        """
        Deletes a tuple in the class relation
        :param cid: class id
        :return: True if success, False otherwise
        """
        query = (sql.SQL("DELETE FROM {} WHERE {} = {}").
                 format(sql.Identifier(self.relation), sql.Identifier('cid'), cid))
        return self.delete(query)