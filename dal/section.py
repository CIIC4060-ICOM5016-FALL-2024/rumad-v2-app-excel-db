import dao


class Section:

    def __init__(self):
        self.dao = dao.DAO()
        self.dao.connect()

    def get_sections(self):
        cursor = self.dao.cursor()
        query = "SELECT * FROM section"
        cursor.execute(query)
        sections = cursor.fetchall()
        return sections

