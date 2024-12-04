import os

from langchain.prompts import ChatPromptTemplate
import requests
import json
from langchain_ollama import OllamaLLM, OllamaEmbeddings


class SyllabusChatBot:
    def __init__(self, history, matches):
        self.model_name = "llama3.1"
        self.model_emb = "nomic-embed-text"
        self.model = OllamaLLM(model=self.model_name, temperature=0.45)
        self.max_retries = 3
        self.conversation_history = history  # To store conversation history
        self.courses = matches

    def get_context(self, question_embedding, course):
        """Retrieve relevant context from the database based on the embedding."""
        headers = {"Content-Type": "application/json"}
        body = {"embedding": str(question_embedding), "course": str(course)}
        attempt = 0
        while attempt < self.max_retries:
            try:
                response = requests.post(
                    "http://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/syllable/embedding",
                    data=json.dumps(body),
                    headers=headers
                )
                response.raise_for_status()
                syllabuses = response.json()
                # Filter out empty or irrelevant responses
                relevant_context = "\n".join(
                    syllabus.get("chunk", "") for syllabus in syllabuses if syllabus.get("chunk"))
                if relevant_context:
                    return relevant_context
                else:
                    print("No relevant context found.")
                    return ""
            except (requests.RequestException, ValueError, KeyError) as e:
                print(f"Attempt {attempt + 1}: Error fetching context: {e}")
                attempt += 1
        return ""

    def generate_answer(self, previous_questions, question, context):
        """Generate an answer based on the question, context, and conversation history."""
        prompt_template = ChatPromptTemplate.from_template(
            """You are an assistant trained to answer questions based on syllabus documents.
            Your role is to help users understand their syllabus, answer questions about courses, and provide information based on the provided documents and conversation history.

            Instructions:
            - Use the provided syllabus documents to answer questions as accurately as possible.
            - If the current question does not mention a specific course, refer to the course mentioned in previous questions.
            - If there is no information available in the documents to answer a question, respond with: "Sorry, I don't know."
            - Keep answers concise and confident, ideally within five sentences. Use bullet points for clarity when listing multiple points.

            Context:
            {documents}

            Current Question:
            {question}

            Previous Questions:
            {previous_questions}

            Answer:
            """
        )
        prompt = prompt_template.format(documents=context, question=question, previous_questions=previous_questions)
        return self.model.invoke(prompt)

    def answer_question(self, question):
        """Answer a syllabus-related question."""

        history = ""
        for i in range(len(self.conversation_history)-1):
            if self.conversation_history[i]['role'] == 'user':
                history += self.conversation_history[i]['content'] + " "

        embedding = OllamaEmbeddings(model=self.model_emb)
        question_embedding = embedding.embed_query(question)
        if not question_embedding:
            return "I couldn't retrieve the embedding to answer your question."

        # Get relevant context for the question based on its embedding
        index = -1
        found = True
        context = ""
        if self.courses and  len(self.courses) > abs(index):
            while len(self.courses[index]) == 0:
                if len(self.courses) > abs(index) + 1:
                    index -= 1
                else:
                    found = False
            if found:
                course = self.courses[index][0]
                print(course)
                if " " not in course:
                    sep = True
                    new_course = ""
                    for i in course:
                        if i.isdigit() and sep:
                            new_course += " "
                            new_course += i
                            sep = False
                        else:
                            new_course += i
                    course = new_course
                context = self.get_context(question_embedding,"%"+ course + '%')
        else:
            found = False

        if not found:
            context = self.get_context(question_embedding, "%")
        if not context:
            return "I couldn't find relevant information to answer your question."

        # Generate and return an answer based on the conversation history and context
        answer = self.generate_answer(history, question, context)

        return answer
