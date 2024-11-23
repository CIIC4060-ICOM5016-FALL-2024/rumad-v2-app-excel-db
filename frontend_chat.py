import streamlit as st
from chat import SyllabusChatBot

# Function to display the chat history and add new messages
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])

st.set_page_config(page_title="Syllabus ChatBot", page_icon="🤖", layout="centered", initial_sidebar_state="auto")

chatbot = SyllabusChatBot(model_name="mistral")

st.title("Ask Questions About Your Syllabus")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about your syllabus!"}
    ]
    display_chat()

if prompt := st.chat_input("Ask a question"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    display_chat()
    with st.chat_message("assistant"):
        typing_placeholder = st.empty()
        typing_placeholder.write("Bot is typing...")
    answer = chatbot.answer_question(prompt)
    typing_placeholder.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})
