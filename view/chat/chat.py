import os
from langchain.prompts import ChatPromptTemplate
import requests
import json
from langchain_ollama import OllamaLLM


class SyllabusChatBot:
    def __init__(self, temp, use_history, history):
        self.model_name = "llama3.1"
        self.model_emb = "nomic-embed-text"
        self.model = OllamaLLM(model=self.model_name, temperature=temp)
        self.ollama_server_url = "http://136.145.116.41:11434/api/chat"  # Ollama server URL
        self.embedding_server_url = "http://136.145.116.41:11434/api/embeddings"  # URL for remote embedding service
        self.max_retries = 3  # Maximum retries for failed requests
        self.use_history = use_history
        self.conversation_history = history  # To store conversation history

    def get_embedding(self, text):
        """Retrieve the embedding for the question from the remote embedding service."""
        headers = {"Content-Type": "application/json"}
        body = {
            "model": self.model_emb,
            "prompt": text,
        }
        attempt = 0
        while attempt < self.max_retries:
            try:
                response = requests.post(self.embedding_server_url, json=body, headers=headers)
                response.raise_for_status()
                embedding = response.json().get("embedding")
                if embedding:
                    return embedding
                else:
                    raise ValueError("Embedding not found in the response.")
            except (requests.RequestException, ValueError, KeyError) as e:
                print(f"Attempt {attempt + 1}: Error requesting embedding: {e}")
                attempt += 1
        return None

    def get_context(self, question_embedding):
        """Retrieve relevant context from the database based on the embedding."""
        headers = {"Content-Type": "application/json"}
        body = {"embedding": str(question_embedding)}
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

    def query_ollama(self, prompt):
        """Send the prompt to the Ollama server and get the response."""
        payload = {
            "model": self.model_name,
            "messages": [{"role": "user", "content": prompt}]
        }
        headers = {"Content-Type": "application/json"}
        try:
            response = requests.post(self.ollama_server_url, json=payload, headers=headers)
            response.raise_for_status()
            lines = response.text.strip().split("\n")
            answer = ""
            for line in lines:
                try:
                    data = json.loads(line)
                    answer += str(data['message']['content'])
                except json.JSONDecodeError as e:
                    print(f"Error parsing JSON: {e}")
            return answer.strip() or "Sorry, I could not generate an answer."
        except requests.exceptions.RequestException as e:
            return f"Error: {str(e)}"

    def generate_answer(self, question, context, history_context):
        """Generate an answer based on the question, context, and conversation history."""
        prompt_template = ChatPromptTemplate.from_template(
            """You are an assistant trained to answer questions based on syllabus documents.
        Your role is to help users understand their syllabus, answer course-related questions, and provide information directly from the provided documents.

        Instructions:
        - Use the provided syllabus documents to answer questions as accurately as possible, only referencing the relevant course information.
        - If the user asks about a specific course (e.g., CIIC 4151), focus on the syllabus information related to that course.
        - If the question is about requisites, grading, or other course-specific information, ensure the answer matches the exact course in the question.
        - Refer to previous conversation history only if it provides relevant context or clarification, and ensure it stays focused on the course in question.
        - If the syllabus does not contain the required information or the question cannot be answered, respond with: "Sorry, I don't know."
        - Keep your answers concise, confident, and ideally under five sentences. Use bullet points for clarity when listing multiple points.
        - Maintain a professional, helpful tone at all times.

        Context:
        {documents}

        Current Question:
        {question}

        Conversation History:
        {conversation}

        Answer:
        """
        )        
        prompt = prompt_template.format(documents=context, question=question, conversation=history_context)
        return self.query_ollama(prompt)

    def answer_question(self, question, local):
        """Answer a syllabus-related question."""
        if local:
            self.embedding_server_url = "http://127.0.0.1:11434/api/embeddings" # Ollama server URL
            self.ollama_server_url = "http://127.0.0.1:11434/api/chat"  # Ollama server URL
        
        history_context = ""
        if self.use_history and self.conversation_history:
            history = ""
            for entry in self.conversation_history:
                history += f"{entry['content']} \n"
        
            history_context = self.get_context(history_embedding)
            if not history_context:
                return "I couldn't find relevant information to answer your question"

            history_embedding = self.get_embedding(history)
            if not history_embedding:
                return "I couldn't retrieve the embedding to answer your question"
        
        question_embedding = self.get_embedding(question)

        if not question_embedding:
            return "I couldn't retrieve the embedding to answer your question."
        

        context = self.get_context(question_embedding)
        if not context:
            return "I couldn't find relevant information to answer your question."
        
        # Generate and return an answer based on the conversation history and context
        answer = self.generate_answer(question, context, history_context)

        return answer