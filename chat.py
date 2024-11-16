from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

from dal.dao.syllabus_dao import SyllabusDAO

model = SentenceTransformer('all-MiniLM-L6-v2')

question = "What are the requisites of the course CIIC 4151 (Design Project)?"

emb = model.encode(question)

dao = SyllabusDAO()

syllabuses = dao.get_from_embedding(str(emb.tolist()))
context = []
for syllabus in syllabuses:
    context.append(syllabus[3])

documents = "\\n".join(c for c in context)

prompt= PromptTemplate(
    template = """You are an assistant for question-answering tasks.
    Use the following documents to answer the question.
    If you don't know the answer, just say that you don't know.
    Use five sentences maximum and keep the answer concise:
    Documents: {documents}
    Question: {question}
    Answer:
    """,
    input_variables = ["question", "documents"]
)

llm = ChatOllama(
    model = "llama3.1",
    temperature=0,
)

rag_chain = prompt | llm | StrOutputParser()

answer = rag_chain.invoke({"question": question, "documents": documents})
print(answer)