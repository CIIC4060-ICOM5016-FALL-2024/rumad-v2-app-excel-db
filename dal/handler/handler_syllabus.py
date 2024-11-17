import json
import os
import re
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from sentence_transformers import SentenceTransformer

from dal.dao.class_dao import ClassDAO
from dal.dao.dao import DAO
from dal.dao.syllabus_dao import SyllabusDAO

class HandlerSyllabus:
    def __init__(self):
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
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
            course_info = os.path.basename(filepath).split('-')
            cname, ccode = course_info[0], course_info[1]
            class_id = self.class_dao.get_class_cid_by_name(cname, ccode)[0][0]

            reader = PdfReader(filepath)
            syllabus_text = [page.extract_text().strip() for page in reader.pages if page.extract_text()]

            processed_data = self.preprocess_syllabus(syllabus_text)
            combined_text = "\n\n".join(processed_data.values())

            splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            split_text = splitter.split_text(combined_text)

            token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)
            token_split_text = [chunk for text in split_text for chunk in token_splitter.split_text(text)]

            for chunk in token_split_text:
                embedding = self.model.encode(chunk)
                self.syllabus_dao.post_syllabus(class_id, json.dumps(embedding.tolist()), chunk)

            print(f"Processed and stored: {filepath}")
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    def load_syllabuses(self):
        """Process all syllabuses in the specified folder."""
        self.dao.delete("TRUNCATE TABLE syllabus RESTART IDENTITY;")
        for syllabus in os.listdir("../../syllabuses"):
            filepath = os.path.join("../../syllabuses", syllabus)
            self.process_file(filepath)


test = HandlerSyllabus()
test.load_syllabuses()