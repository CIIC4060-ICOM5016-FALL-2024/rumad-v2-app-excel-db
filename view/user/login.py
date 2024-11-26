import streamlit as st
from streamlit_option_menu import option_menu
import requests

class Login:

    def __init__(self, cookies):
        self.cookies = cookies

    def login_widget(self):
        with st.form("Login Form", clear_on_submit=True):
            st.subheader("Login to Your Account")
            username = st.text_input("Username", max_chars=20, placeholder="Enter your username")
            password = st.text_input("Password", type='password', placeholder="Enter your password")
            login_button = st.form_submit_button("Login")

            if login_button:
                # Send login request to the backend
                data = {"username": username, "password": password}
                response = requests.post("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user/login", json=data)

                if response.status_code == 200:
                    user_data = response.json()
                    st.session_state["LOGGED_IN"] = True
                    st.session_state["USERNAME"] = user_data["username"]

                    self.cookies["LOGGED_IN"] = "True"
                    self.cookies["USERNAME"] = user_data["username"]
                    self.cookies.save()

                    st.success("Login successful!", icon="✅")
                    return True
                else:
                    error_message = response.json().get("error", "An error occurred")
                    st.error(error_message, icon="❌")
                    return False

    def sign_up_widget(self):
        with st.form("Sign Up Form", clear_on_submit=True):
            st.subheader("Create a New Account")
            username = st.text_input("Username", max_chars=20, placeholder="Choose a username")
            password = st.text_input("Password", type='password', placeholder="Choose a password")
            email = st.text_input("Email", placeholder="Enter your email")

            sign_up_button = st.form_submit_button("Sign Up")

            if sign_up_button:
                try:
                    data = {"username": username, "password": password, "email": email}
                    response = requests.post("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user", json=data)

                    if response.status_code == 201:
                        st.session_state["LOGGED_IN"] = True
                        st.session_state["USERNAME"] = username
                        self.cookies["LOGGED_IN"] = "True"
                        self.cookies["USERNAME"] = username
                        self.cookies.save()
                        st.success("Account created successfully!", icon="✅")
                        return True

                    else:
                        error_message = response.json().get("error", "An error occurred")
                        st.error(error_message, icon="❌")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}", icon="❌")

    def logout_widget(self):
        if st.button("Logout", key="logout_button"):
            self.cookies["LOGGED_IN"] = "False"
            self.cookies["USERNAME"] = ""
            st.session_state["LOGGED_IN"] = False
            st.session_state["USERNAME"] = None
            st.rerun()

    def nav_sidebar(self):
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title='Navigation',
                menu_icon='list-columns-reverse',
                icons=['box-arrow-in-right', 'person-plus', 'x-circle', 'arrow-counterclockwise'],
                options=['Login', 'Create Account'],
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"}
                }
            )
        return selected_option

    def build_login_ui(self):
        if "LOGGED_IN" not in st.session_state:
            st.session_state["LOGGED_IN"] = False

        selected_option = self.nav_sidebar()

        if selected_option == "Login":
            if self.login_widget():
                st.rerun()
        elif selected_option == "Create Account":
            if self.sign_up_widget():
                st.rerun()
        if st.session_state["LOGGED_IN"]:
            self.logout_widget()

        return st.session_state["LOGGED_IN"]

    def get_username(self):
        return st.session_state["USERNAME"]
