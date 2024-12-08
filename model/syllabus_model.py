import os
import re
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from langchain_ollama import OllamaEmbeddings
from flask import jsonify

from dal.class_dao import ClassDAO
from dal.dao import DAO
from dal.syllabus_dao import SyllabusDAO

attributes = ["courseid", "embedding_text", "chunk"]


class SyllabusModel:
    def __init__(self):
        self.model = "nomic-embed-text"
        self.class_dao = ClassDAO()
        self.syllabus_dao = SyllabusDAO()
        self.dao = DAO()

    def preprocess_syllabus(self, data):
        """Preprocess syllabus text by extracting key sections."""
        raw_text = " ".join(data)

        # Define patterns to match sections
        patterns = {
            "General Information": r"General Information:.*?(?=Course Description:)",
            "Course Description": r"Course Description:.*?(?=Pre/Co-requisites and other requirements:)",
            "Pre/Co-requisites and other requirements": r"Pre/Co-requisites and other requirements:.*?(?=Course Objectives:)",
            "Course Objectives": r"Course Objectives.*?(?=Instructional Strategies:)",
            "Instructional Strategies": r"Instructional Strategies:.*?(?=Minimum or Required Resources Available:)",
            "Minimum or Required Resources Available": r"Minimum or Required Resources Available:.*?(?=Course time frame and thematic outline)",
            "Course time frame and thematic outline": r"Course time frame and thematic outline.*?(?=Grading System)",
            "Grading System": r"Grading System.*?(?=Evaluation Strategies)",
            "Evaluation Strategies": r"Evaluation Strategies.*?(?=Bibliography)",
            "Bibliography": r"Bibliography.*?(?=Course Outcomes)",
            "Course Outcomes": r"Course Outcomes.*?(?=According to Law 51|Academic Integrity)"
        }

        cleaned_data = {}
        for section, pattern in patterns.items():
            match = re.search(pattern, raw_text, re.DOTALL)
            if match:
                cleaned_section = re.sub(r'\s+', ' ', match.group(0)).strip()
                cleaned_data[section] = cleaned_section

        return cleaned_data

    def process_file(self, filepath):
        """Process a single syllabus file and store it in the database."""
        try:
            course_info = (os.path.basename(filepath)[:-4] + " ").split('-')
            cname, ccode = course_info[0], course_info[1]
            class_id = self.class_dao.get_class_cid_by_name(cname, ccode)[0][0]

            reader = PdfReader(filepath)
            syllabus_text = [page.extract_text().strip() for page in reader.pages if page.extract_text()]

            processed_data = self.preprocess_syllabus(syllabus_text)
            combined_text = "\n\n".join(processed_data.values())

            splitter = RecursiveCharacterTextSplitter(
                chunk_size=800,
                chunk_overlap=80,
                length_function=len,
                is_separator_regex=False,
            )
            if len(combined_text) > 0:
                split_text = splitter.split_text(combined_text)
            else:
                split_text = splitter.split_text("\n\n".join(syllabus_text))

            token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
            token_split_text = [chunk for text in split_text for chunk in token_splitter.split_text(text)]
            embedding = OllamaEmbeddings(model=self.model)
            for chunk in token_split_text:
                chunk = cname + " " + ccode + " " + ' '.join(course_info[2:]).upper() + chunk
                emb = embedding.embed_query(chunk)
                self.syllabus_dao.post_syllabus(class_id, str(emb), chunk)

            print(f"Processed and stored: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    def load_syllabuses(self):
        """Process all syllabuses in the specified folder."""
        self.dao.delete("TRUNCATE TABLE syllabus RESTART IDENTITY;")
        for syllabus in os.listdir("../syllabuses"):
            filepath = os.path.join("../syllabuses", syllabus)
            self.process_file(filepath)

    @staticmethod
    def jsonify_response(response):
        """
        Turns a list of tuples into a JSON response if response has True.
        @param response: A list of tuples or a single tuple
        @return: JSON and HTTP response code
        """
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500  # Internal Server Error

        result = []
        for syllabus in response:
            result_dict = {
                "chunkid": syllabus[0],
                "courseid": syllabus[1],
                "embedding_text": syllabus[2],
                "chunk": syllabus[3],
            }
            result.append(result_dict)

        return jsonify(result)

    def get_all_syllabus(self):
        """
        Get all syllabus from the syllabus relation database.
        @return: JSON and HTTP response code
        """
        response = self.syllabus_dao.get_all_syllabus()
        return self.jsonify_response(response)

    def post_syllabus(self, data):
        """
        Create a new syllabus tuple in the syllabus relation database.
        @param data: a list with syllabus attributes to be added
        @return: JSON and HTTP response code
        """
        # Check that all attributes are present
        try:
            syllabus_attributes = {key: data[key] for key in attributes}
        except KeyError as e:  # bad request
            missing_attribute = e.args[0]
            return jsonify(f'Missing required attribute: {missing_attribute}'), 400

        course_id = syllabus_attributes["courseid"]
        embedding_text = syllabus_attributes["embedding_text"]
        chunk = syllabus_attributes["chunk"]

        response = self.syllabus_dao.post_syllabus(course_id, embedding_text, chunk)

        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500

        return jsonify(f'Syllabus has been created with chunk_id: {response[1]}'), 201

    def get_syllabus_by_id(self, chunk_id):
        """
        Get a syllabus by id from the syllabus relation database.
        @param chunk_id: chunk id
        @return: JSON and HTTP response code
        """
        response = self.syllabus_dao.get_syllabus_by_chunk_id(int(chunk_id))
        return self.jsonify_response(response)

    def get_syllabus_by_embedding(self, data):
        """
        Get all tuples from the syllabus relation by similarity of the embedding
        @param data: data
        @return: JSON and HTTP response code
        """
        embedding = data.get("embedding")
        response = self.syllabus_dao.get_from_embedding(embedding)
        return self.jsonify_response(response)

    def put_syllabus_by_id(self, chunk_id, data):
        """
        Update a syllabus by id from the syllabus relation database.
        @param chunk_id: chunk id
        @param data: attributes to be updated
        @return: JSON and HTTP response code
        """
        response = self.syllabus_dao.put_syllabus_by_chunk_id(int(chunk_id), data)
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500
        return jsonify(f'Syllabus {chunk_id} has been updated'), 200

    def delete_syllabus(self, chunk_id):
        """
        Delete a syllabus from the syllabus relation database.
        @param chunk_id: chunk id
        @return: JSON and HTTP response code
        """
        response = self.syllabus_dao.delete(int(chunk_id))
        if False in response:
            return jsonify(f'{response[1]}: {response[2]}'), 500
        return jsonify(f'Syllabus {chunk_id} has been deleted'), 200

if __name__ == '__main__':
    s = SyllabusModel()
    s.load_syllabuses()