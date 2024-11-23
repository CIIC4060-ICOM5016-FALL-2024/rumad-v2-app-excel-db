from dal.dao.syllabus_dao import SyllabusDAO
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM

class SyllabusChatBot:
    def __init__(self, model_name="mistral"):
        self.model_emb = "nomic-embed-text"
        self.model = OllamaLLM(model=model_name)
        self.syllabus_dao = SyllabusDAO()
        self.history = []

    def get_context(self, question_embedding):
        """Retrieve relevant context from the database based on the embedding."""
        syllabuses = self.syllabus_dao.get_from_embedding(str(question_embedding))
        return "\n".join(syllabus[3] for syllabus in syllabuses)

    def generate_answer(self, question, context):
        """Generate an answer based on the question, context, and conversation history."""
        history_text = "\n".join(f"User: {q}\nBot: {a}" for q, a in self.history)
        prompt_template = ChatPromptTemplate.from_template(
            """You are an assistant trained to answer questions based strictly on the provided syllabus documents.
            You will be given several documents. Each document corresponds to a different course or subject. 
            Your task is to find the syllabus that is relevant to the question asked and use only that syllabus to provide the answer.
            If the question asks about a specific course, focus only on the syllabus for that course.
            If the relevant syllabus cannot be identified or if the question is unclear, you must respond with 'I don't know.'
            Do **not** make up information. Always base your answer strictly on the syllabus content provided.
            Keep your answer concise and no more than five sentences.
            Conversation history: {history}
            Documents: {documents}
            Current Question: {question}
            Answer:
            """
        )
        prompt = prompt_template.format(history=history_text, documents=context, question=question)
        return self.model.invoke(prompt)

    def answer_question(self, question):
        """Answer a syllabus-related question."""
        embedding = OllamaEmbeddings(model=self.model_emb)
        question_embedding = embedding.embed_query(question)
        context = self.get_context(question_embedding)
        if not context:
            answer = "I couldn't find relevant information to answer your question."
        else:
            answer = self.generate_answer(question, context)
        self.history.append((question, answer))
        return answer