import streamlit as st
from streamlit_option_menu import option_menu
import requests

class Login:
    """
    A login/sign up page for Streamlit with side navigation bar.
    """
    def __init__(self, cookies):
        self.cookies = cookies

    def login_widget(self):
        """
        Displays the login form and checks credentials.
        """
        with st.form("Login Form", clear_on_submit=True):
            st.subheader("Login to Your Account")
            username = st.text_input("Username", max_chars=20, placeholder="Enter your username")
            password = st.text_input("Password", type='password', placeholder="Enter your password")
            login_button = st.form_submit_button("Login")

            if login_button:
                try:
                    response = requests.get(f"http://127.0.0.1:5000/excel_db/user/{username}")
                    if response.status_code == 200:
                        user_data = response.json()
                        if user_data[0]["password"] == password:
                            st.session_state["LOGGED_IN"] = True
                            st.session_state["USERNAME"] = username
                            self.cookies["LOGGED_IN"] = "True"
                            self.cookies["USERNAME"] = username
                            self.cookies.save()
                            return True
                        else:
                            st.error("Invalid Username or Password", icon="❌")
                    else:
                        st.error("User not found or server error occurred.", icon="❌")
                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}", icon="❌")
        return False

    def sign_up_widget(self):
        """
        Displays the sign-up form to create a new account.
        """
        with st.form("Sign Up Form", clear_on_submit=True):
            st.subheader("Create a New Account")
            username = st.text_input("Username", max_chars=20, placeholder="Choose a username")
            password = st.text_input("Password", type='password', placeholder="Choose a password")
            email = st.text_input("Email", placeholder="Enter your email")

            sign_up_button = st.form_submit_button("Sign Up")

            if sign_up_button:
                try:
                    data = {"username": username, "password": password, "email": email}
                    response = requests.post("http://127.0.0.1:5000/excel_db/user", json=data)
                    print(response)

                    print(response.status_code)

                    if response.status_code == 201:
                        st.session_state["LOGGED_IN"] = True
                        st.session_state["USERNAME"] = username

                        self.cookies["LOGGED_IN"] = "True"
                        self.cookies["USERNAME"] = username
                        self.cookies.save()

                        st.success("Account created successfully!", icon="✅")
                        return True
                    else:
                        st.error(f"Error: {response.status_code}. Please try again later.", icon="❌")

                except requests.exceptions.RequestException as e:
                    st.error(f"An error occurred: {str(e)}", icon="❌")

    def logout_widget(self):
        """
        Displays a logout button.
        """
        if st.button("Logout", key="logout_button"):
            self.cookies["LOGGED_IN"] = "False"
            self.cookies["USERNAME"] = ""
            st.session_state["LOGGED_IN"] = False
            st.session_state["USERNAME"] = None
            st.rerun()

    def nav_sidebar(self):
        """
        Creates the side navigation bar.
        """
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
        """
        Builds the entire UI with navigation options.
        """
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
