from dao import DAO

class SectionDAO(DAO):

    def __init__(self):
        super().__init__()

    def get_sections(self):
        cursor = self.cursor()
        query = "SELECT * FROM section"
        cursor.execute(query)
        sections = cursor.fetchall()
        return sections
