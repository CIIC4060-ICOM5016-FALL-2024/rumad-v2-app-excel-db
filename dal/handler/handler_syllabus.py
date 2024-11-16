import json
from os import listdir
from pypdf import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter, SentenceTransformersTokenTextSplitter
from sentence_transformers import SentenceTransformer

from dal.dao.class_dao import ClassDAO
from dal.dao.dao import DAO
from dal.dao.syllabus_dao import SyllabusDAO

model = SentenceTransformer("all-MiniLM-L6-v2")

syllabuses = listdir('../../syllabuses')

classDAO = ClassDAO()
syllabusDAO = SyllabusDAO()
dao = DAO()
dao.delete("TRUNCATE TABLE syllabus RESTART IDENTITY;")

for syllabus in syllabuses:
    name = "../../syllabuses/" + syllabus
    course = name.split('-')
    cname = course[0].split('/')[-1]
    ccode = course[1]
    id = classDAO.get_class_cid_by_name(cname, ccode)[0][0]
    reader = PdfReader(name)
    syllabus_text = [page.extract_text().strip() for page in reader.pages]

    syllabus_text = [text for text in syllabus_text if text]

    spliter = RecursiveCharacterTextSplitter(
        separators=["\n\n", "\n", ". ", " ", ""],
        chunk_size=1000,
        chunk_overlap=0
    )
    split_text = spliter.split_text('\n\n'.join(syllabus_text))

    token_splitter = SentenceTransformersTokenTextSplitter(chunk_overlap=0, tokens_per_chunk=256)

    token_split_text = []
    for chunk in split_text:
        token_split_text += token_splitter.split_text(chunk)

    # Insert syllabus to table
    for chunk in token_split_text:
        embedding = model.encode(chunk)
        # insert chunk in to table
        syllabusDAO.post_syllabus(id, json.dumps(embedding.tolist()), chunk)

    print(f"Done file: {name}")
