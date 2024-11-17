from sentence_transformers import SentenceTransformer
from langchain_ollama import ChatOllama
from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dal.dao.syllabus_dao import SyllabusDAO
import json

class SyllabusChatBot:
    def __init__(self, model_name="all-MiniLM-L6-v2", llm_model="llama3.1"):
        self.model = SentenceTransformer(model_name)
        self.llm = ChatOllama(model=llm_model, temperature=0)
        self.syllabus_dao = SyllabusDAO()

    def get_context(self, question_embedding):
        """Retrieve relevant context from the database based on the embedding."""
        syllabuses = self.syllabus_dao.get_from_embedding(json.dumps(question_embedding.tolist()))
        return "\n".join(syllabus[3] for syllabus in syllabuses)

    def generate_answer(self, question, context):
        """Generate an answer based on the question and context."""
        prompt = PromptTemplate(
            template="""You are an assistant for question-answering tasks.
            Use the following documents to answer the question.
            If you don't know the answer, just say that you don't know.
            Use five sentences maximum and keep the answer concise:
            Documents: {documents}
            Question: {question}
            Answer:
            """,
            input_variables=["question", "documents"]
        )
        rag_chain = prompt | self.llm | StrOutputParser()
        return rag_chain.invoke({"question": question, "documents": context})

    def answer_question(self, question):
        """Answer a syllabus-related question."""
        question_embedding = self.model.encode(question)
        context = self.get_context(question_embedding)
        # print(context)
        if not context:
            return "I couldn't find relevant information to answer your question."
        return self.generate_answer(question, context)

# Example usage:
if __name__ == "__main__":
    bot = SyllabusChatBot()
    question = "Tell me at least 3 topics that are taught in the introduction to database (CIIC4060) course?"
    answer = bot.answer_question(question)
    print(answer)
