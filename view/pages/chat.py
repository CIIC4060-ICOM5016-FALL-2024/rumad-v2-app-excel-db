from gtts import gTTS
import streamlit as st
from chat.chat import SyllabusChatBot

def initialize_session_state():
    """Initialize session state variables."""
    if "chats" not in st.session_state:
        st.session_state.chats = {"Chat 1": []}  # Dictionary to store chat histories
    if "active_chat" not in st.session_state:
        st.session_state.active_chat = "Chat 1"  # Set Chat 1 as the active chat

initialize_session_state()

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

    with st.chat_message("assistant"):
        st.write("""Hello! I'm here to help you understand your syllabus and answer any course-related questions.
                 Which specific course would you like to know more about?""")

    def display_chat():
        """Display the chat history."""
        for message in chat_history:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                
    with st.sidebar:
        st.subheader("Chat Settings")
        use_history = st.toggle("Enable History")
        local = st.toggle("Run Ollama locally")
        temp = st.slider("Chat temp (Deterministic--> Creative)", 0.00, 1.00, 0.45, 0.05)
        
    display_chat()
    
    if prompt := st.chat_input("Ask a question"):
        chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.write("Bot is typing...")
            chatbot = SyllabusChatBot(temp, use_history, chat_history)
            answer = chatbot.answer_question(prompt, local)
            typing_placeholder.write(answer)
            chat_history.append({"role": "assistant", "content": answer})
            audio_file_path = f"{chat_id}audio{len(chat_history)}.mp3"
            tts = gTTS(text=answer, lang="en")
            tts.save(audio_file_path)
            st.audio(audio_file_path, format="audio/mp3")

st.title("RUMAD V2.0 🤖")

initialize_session_state()

with st.sidebar:
    st.subheader("Manage Chats")
    if st.button("Create New Chat"):
        create_chat()

    # Display current chats
    if st.session_state.chats:
        st.session_state.active_chat = st.selectbox(
            "Select a Chat",
            options=list(st.session_state.chats.keys()),
            index=0 if st.session_state.active_chat is None else list(st.session_state.chats.keys()).index(
                st.session_state.active_chat)
        )

        if st.button("Delete Selected Chat"):
            delete_chat(st.session_state.active_chat)

# Display the active chatbot
if st.session_state.active_chat:
    st.subheader(f"{st.session_state.active_chat}")
    chatbot(st.session_state.active_chat)
else:
    st.write("No active chat. Create a new chat to start!")