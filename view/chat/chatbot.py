import os
from gtts import gTTS
import streamlit as st
from chat.chat import SyllabusChatBot

# List of courses
courses = ['CIIC 4998', 'CIIC4998', 'Undergraduate Research', 'CIIC 3075', 'CIIC3075',
           'Foundations of Computing', 'INSO 4151', 'INSO4151', 'Software Engineering',
           'INSO 4116', 'INSO4116', 'Software Design', 'CIIC 3081', 'CIIC3081',
           'Computer Architecture', 'CIIC 5017', 'CIIC5017', 'Operating Systems',
           'CIIC 4030', 'CIIC4030', 'Programming Languages', 'CIIC 5015', 'CIIC5015',
           'Artificial Intelligence', 'CIIC 4060', 'CIIC4060', 'Database Systems',
           'CIIC 5130', 'CIIC5130', 'Cloud Computing']

def initialize_session_state():
    """Initialize session state variables."""
    if "chats" not in st.session_state:
        st.session_state.chats = {}  # Dictionary to store chat histories
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = None  # Active chat ID

def create_chat():
    """Create a new chat and add it to the session state."""
    chat_id = f"Chat {len(st.session_state.chats) + 1}"
    st.session_state.chats[chat_id] = []  # Initialize with an empty chat history
    st.session_state.active_chat = chat_id  # Set the newly created chat as active

def delete_chat(chat_id):
    """Delete a chat and remove it from the session state."""
    if chat_id in st.session_state.chats:
        del st.session_state.chats[chat_id]
        # Set active chat to None or to another available chat
        st.session_state.active_chat = next(iter(st.session_state.chats), None)

def chatbot(chat_id):
    """Chatbot interaction for a specific chat."""
    chat_history = st.session_state.chats[chat_id]

    def display_chat():
        """Display the chat history."""
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])

    display_chat()

    if prompt := st.chat_input("Ask a question"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.write("Bot is typing...")
            chatbot = SyllabusChatBot(chat_history, [])
            answer = chatbot.answer_question(prompt)
            typing_placeholder.write(answer)
            chat_history.append({"role": "assistant", "content": answer})
            audio_file_path = f"{chat_id}_audio_{len(chat_history)}.mp3"
            tts = gTTS(text=answer, lang="en")
            tts.save(audio_file_path)
            st.audio(audio_file_path, format="audio/mp3")
