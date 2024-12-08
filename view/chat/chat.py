import os

from langchain.prompts import ChatPromptTemplate
import requests
import json
from langchain_ollama import OllamaLLM


class SyllabusChatBot:
    def __init__(self, history, matches):
        self.model_name = "llama3.1"
        self.model_emb = "nomic-embed-text"
        self.model = OllamaLLM(model=self.model_name, temperature=0.45)
        self.ollama_server_url = "http://136.145.116.41:11434/api/chat"  # Ollama server URL
        self.embedding_server_url = "http://136.145.116.41:11434/api/embeddings"  # URL for remote embedding service
        self.max_retries = 3  # Maximum retries for failed requests
        # self.conversation_history = history  # To store conversation history
        # self.courses = matches

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

    def generate_answer(self, question, context):
        """Generate an answer based on the question, context, and conversation history."""
        prompt_template = ChatPromptTemplate.from_template(
            """You are an assistant trained to answer questions based on syllabus documents.
            Your role is to help users understand their syllabus, answer questions about courses, and provide information based on the provided documents.

            Instructions:
            - Use the provided syllabus documents to answer questions as accurately as possible.
            - If there is no information available in the documents to answer a question, respond with: "Sorry, I don't know."
            - Keep answers concise and confident, ideally within five sentences. Use bullet points for clarity when listing multiple points.

            Context:
            {documents}

            Current Question:
            {question}

            Answer:
            """
        )
        prompt = prompt_template.format(documents=context, question=question)
        return self.query_ollama(prompt)

    def answer_question(self, question, local):
        """Answer a syllabus-related question."""
        if local:
            self.embedding_server_url = "http://127.0.0.1:11434/api/embeddings" # Ollama server URL
            self.ollama_server_url = "http://127.0.0.1:11434/api/chat"  # Ollama server URL
        
        question_embedding = self.get_embedding(question)

        if not question_embedding:
            return "I couldn't retrieve the embedding to answer your question."

        context = self.get_context(question_embedding)
        print(context)
        if not context:
            return "I couldn't find relevant information to answer your question."

        # Generate and return an answer based on the conversation history and context
        answer = self.generate_answer(question, context)

        return answer
