from dao import DAO

class Section(DAO):

    def __init__(self):
        super().__init__()
        self.connect()

    def get_sections(self):
        cursor = self.cursor()
        query = "SELECT * FROM section"
        cursor.execute(query)
        sections = cursor.fetchall()
        return sections
