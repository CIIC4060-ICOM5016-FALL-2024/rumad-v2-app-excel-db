import os

import streamlit as st

from chat.chat import SyllabusChatBot

courses = []
if len(os.listdir(os.getcwd() + "/syllabuses")) != 35:
    for syllabus in os.listdir(os.getcwd() + "/syllabuses"):
        filepath = os.path.join("../../syllabuses", syllabus)
        course_info = (os.path.basename(filepath)[:-4] + " ").split('-')
        courses.append(str(course_info[0]) + " " + str(course_info[1]))
        courses.append(str(course_info[0]) + str(course_info[1]))
        for i in range(2,len(course_info)-1):
            courses.append(' '.join(course_info[2:2 + i]))
else:
    courses = ['CIIC 4998', 'CIIC4998', 'Undergraduate Research ', 'CIIC 3075', 'CIIC3075', 'Foundations of', 'Foundations of Computing ', 'INSO 4151', 'INSO4151', 'Software Engineering', 'Software Engineering Project', 'Software Engineering Project I ', 'INSO 4116', 'INSO4116', 'Software Design ', 'CIIC 3081', 'CIIC3081', 'Computer Architecture', 'Computer Architecture I ', 'CIIC 5017', 'CIIC5017', 'Operating Systems', 'Operating Systems and', 'Operating Systems and Network', 'Operating Systems and Network Administration', 'Operating Systems and Network Administration and', 'Operating Systems and Network Administration and Security ', 'CIIC 5110', 'CIIC5110', 'Bioinformatics Algorithms ', 'CIIC 5140', 'CIIC5140', 'Big Data', 'Big Data Analytics ', 'CIIC 5019', 'CIIC5019', 'High Performance', 'High Performance Computing ', 'CIIC 4030', 'CIIC4030', 'Programming Languages ', 'INSO 4101', 'INSO4101', 'Introduction to', 'Introduction to Software', 'Introduction to Software Engineering ', 'CIIC 5029', 'CIIC5029', 'Compilers Development ', 'CIIC 4025', 'CIIC4025', 'Analysis and', 'Analysis and Design', 'Analysis and Design of', 'Analysis and Design of Algorithms ', 'CIIC 5120', 'CIIC5120', 'Virtual Machines ', 'CIIC 5150', 'CIIC5150', 'Machine Learning', 'Machine Learning Algorithms ', 'INSO 4115', 'INSO4115', 'Software Engineering', 'Software Engineering Requirements ', 'CIIC 5015', 'CIIC5015', 'Artificial Intelligence ', 'INSO 5111', 'INSO5111', 'Introduction to', 'Introduction to Human', 'Introduction to Human Computer', 'Introduction to Human Computer Interaction ', 'CIIC 4070', 'CIIC4070', 'Computer Networks ', 'CIIC 3015', 'CIIC3015', 'Introduction to', 'Introduction to Computer', 'Introduction to Computer Programming', 'Introduction to Computer Programming I ', 'INSO 4995', 'INSO4995', 'CIIC 4082', 'CIIC4082', 'Computer Architecture', 'Computer Architecture II ', 'CIIC 4050', 'CIIC4050', 'Operating Systems ', 'CIIC 4010', 'CIIC4010', 'Advanced Programming ', 'CIIC 5018', 'CIIC5018', 'Cryptography and', 'Cryptography and Network', 'Cryptography and Network Security ', 'CIIC 4151', 'CIIC4151', 'Senior Design', 'Senior Design Project', 'Senior Design Project I ', 'CIIC 5995', 'CIIC5995', 'Selected Topics ', 'CIIC 4020', 'CIIC4020', 'Data Structures ', 'CIIC 4995', 'CIIC4995', 'Engineering Practice', 'Engineering Practice for', 'Engineering Practice for Coop', 'Engineering Practice for Coop Students ', 'CIIC 5045', 'CIIC5045', 'Automata and', 'Automata and Formal', 'Automata and Formal Languages ', 'INSO 5118', 'INSO5118', 'Software Engineering', 'Software Engineering Project', 'Software Engineering Project Management ', 'INSO 4998', 'INSO4998', 'Undergraduate Research', 'Undergraduate Research in', 'Undergraduate Research in Software', 'Undergraduate Research in Software Engineering ', 'CIIC 4060', 'CIIC4060', 'Database Systems ', 'INSO 4117', 'INSO4117', 'Software Reliability', 'Software Reliability Testing ', 'CIIC 5130', 'CIIC5130', 'Cloud Computing', 'Cloud Computing Infrastructures ']

matches = []
def chatbot():
    global matches
    # Function to display the chat history and add new messages
    def display_chat():
        global matches
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.write(message["content"])
                if message['role'] == 'user':
                    matches.append([course for course in courses if course.strip() in message['content']])

    st.title("Ask Questions About Your Syllabus")
    with st.chat_message("assistant"):
        st.write("Ask me a question about your syllabus!")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    chatbot = SyllabusChatBot(st.session_state.messages, matches)

    if prompt := st.chat_input("Ask a question"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        display_chat()
        chatbot.courses = matches
        with st.chat_message("assistant"):
            typing_placeholder = st.empty()
            typing_placeholder.write("Bot is typing...")
        answer = chatbot.answer_question(prompt)
        typing_placeholder.write(answer)
        st.session_state.messages.append({"role": "assistant", "content": answer})
