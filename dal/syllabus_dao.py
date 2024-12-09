from dal.dao import DAO

class SyllabusDAO(DAO):

    def __init__(self):
        super().__init__()

    # POST
    def post_syllabus(self, cid: int, embedding: str, chunk: str):
        """
        Creates a tuple in the syllabus relation
        :param cid: class id
        :param embedding: syllabus embedding
        :param chunk: syllabus chunk (text)
        :return: True if success, False otherwise
        """
        query = """INSERT INTO syllabus (courseid, embedding_text, chunk) VALUES (%s, %s, %s)
        RETURNING chunkid"""
        values = [cid, embedding, chunk]
        return self.create(query, values)

    # GET
    def get_all_syllabus(self):
        """
        Gets all tuples from the syllabus relation
        :return: a list of tuples, or None if failed
        """
        query = "SELECT * FROM syllabus"
        return self.read(query)

    def get_syllabus_by_chunk_id(self, chunk_id: int):
        """
        Gets all tuples from the syllabus relation by chunk_id
        :param chunk_id: syllabus id
        :return: a list with a single tuple, or None if failed
        """
        query = "SELECT * FROM syllabus WHERE chunkid = %s"
        values = [chunk_id, ]
        return self.read( query, values)

    def get_from_embedding(self, emb: str):
        """
        Get all tuples from the syllabus relation by similarity of the embedding
        @param emb: query embedding
        @return: a list of tuples, or None if failed
        """

        query = """SELECT chunkid, courseid, embedding_text <=> %s as distance, chunk 
                    FROM syllabus 
                    ORDER BY distance 
                    LIMIT 5"""
        values = [emb, ]
        return self.read(query, values)

    # PUT
    def put_syllabus_by_chunk_id(self, chunk_id: int, data):
        """
        Updates a syllabus tuple in the syllabus relation
        :param chunk_id: syllabus id
        :param data: attributes to be updated
        :return: True if success, False otherwise
        """
        new = ', '.join([f"{key} = %s" for key in data.keys()])
        values = tuple(data.values()) + (chunk_id, )
        query = f"UPDATE syllabus SET {new} WHERE chunkid = %s"
        return self.update(query, values)

    # DELETE
    def delete_section(self, chunk_id: int):
        """
        Deletes a tuple in syllabus relation
        :param chunk_id: syllabus id
        :return: True if success, False otherwise
        """
        query = "DELETE FROM syllabus WHERE chunkid = %s"
        values = [chunk_id]
        return self.delete(query, values)
