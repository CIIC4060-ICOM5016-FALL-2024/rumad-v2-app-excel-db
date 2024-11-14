from dal.dao.dao import DAO


class SyllabusDAO(DAO):
    def __init__(self):
        super().__init__()

    # POST
    def post_syllabus(self, cid, embedding, chunk):
        query = "INSERT INTO syllabus (courseid, embedding_text, chunk) VALUES (%s, %s, %s)"
        values = [cid, embedding, chunk]
        return self.create(query, values)

    # GET
    def get_all_syllabus(self):
        query = "SELECT * FROM syllabus"
        return self.read(query)

    def get_syllabus_by_chunk_id(self, chunk_id: int):
        query = "SELECT * FROM syllabus WHERE sid = %s"
        return self.read(
            query,
            [
                chunk_id,
            ],
        )

    # PUT
    def put_syllabus_by_chunkid(self, chunkid: int, data):
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (chunkid, )
        query = f"UPDATE syllabus SET {new} WHERE chunkid = %s"
        return self.update(query, values)

    # DELETE
    def delete_section(self, chunkid: int):
        query = "DELETE FROM syllabus WHERE chunkid = %s"
        values = [chunkid]
        return self.delete(query, values)
