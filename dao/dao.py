from config.dbconfig import pg_config
import psycopg2

class DAO:
    def __init__(self):
        url = ("dbname=%s password=%s host=%s port=%s user=%s" %
               (pg_config['dbname'],
                pg_config['password'],
                pg_config['host'],
                pg_config['port'],
                pg_config['user'])
               )
        self.connection = psycopg2.connect(url)

    # TODO Class CRUD
    def topLeastClasses(self):
        cursor = self.connection.cursor()
        query = "select distinct section.cid,count(*) as section_count, class.cdesc from section inner join class on section.cid = class.cid group by section.cid , class.cdesc order by section_count limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def totalSections(self):
        cursor = self.connection.cursor()
        query = "select years as year,count(*) as total_sections from section group by years order by total_sections;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    def topPreRequisite(self):
        cursor = self.connection.cursor()
        query = "select count(*), requisite.requid, class.cdesc from requisite inner join class on requisite.requid = class.cid where prereq = 'true' and requid != 37 group by requisite.requid, class.cdesc order by count(*) desc limit 3;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        cursor.close()
        return result

    # TODO Requisite CRUD

    # TODO Section CRUD

    # TODO Meeting CRUD

    # TODO Room CRUD