from langchain.chains import ConversationChain
from langchain.prompts import ChatPromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM
import requests
import json

class SyllabusChatBot:
    def __init__(self, model_name="llama3.1"):
        self.model_emb = "nomic-embed-text"
        self.model = OllamaLLM(model="llama3.1", temperature=0.8)
        self.conversation = ConversationChain(llm=self.model)

    def get_context(self, question_embedding):
        """Retrieve relevant context from the database based on the embedding."""
        try:
            headers = {"Content-Type": "application/json"}
            body = {
                "embedding": str(question_embedding)
            }
            response = requests.post(
                f"https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/syllable/embedding",
                data=json.dumps(body),
                headers=headers
            )
            response.raise_for_status()
            syllabuses = response.json()
            return "\n".join(syllabus['chunk'] for syllabus in syllabuses)
        except requests.RequestException as e:
            print(f"An error occurred: {e}")
            return ""
        except (KeyError, IndexError, TypeError) as e:
            print(f"An error occurred while processing the response: {e}")
            return ""

    def generate_answer(self, question, context):
        """Generate an answer based on the question, context, and conversation history."""
        prompt_template = ChatPromptTemplate.from_template(
            """You are an assistant trained to answer questions based strictly on the provided syllabus documents.
            You will be given several documents. Each document corresponds to a different course or subject. 
            Your task is to find the syllabus that is relevant to the question asked and use only that syllabus to provide the answer.
            If the question asks about a specific course, focus only on the syllabus for that course.
            If the relevant syllabus cannot be identified or if the question is unclear, you must respond with 'I don't know.'
            Do **not** make up information. Always base your answer strictly on the syllabus content provided.
            Keep your answer concise and no more than five sentences.
            Documents: {documents}
            Current Question: {question}
            Answer:
            """
        )
        prompt = prompt_template.format(documents=context, question=question)
        return self.conversation.predict(input=prompt)

    def answer_question(self, question):
        """Answer a syllabus-related question."""
        embedding = OllamaEmbeddings(model=self.model_emb)
        question_embedding = embedding.embed_query(question)
        context = self.get_context(question_embedding)
        if not context:
            answer = "I couldn't find relevant information to answer your question."
        else:
            answer = self.generate_answer(question, context)
        return answer