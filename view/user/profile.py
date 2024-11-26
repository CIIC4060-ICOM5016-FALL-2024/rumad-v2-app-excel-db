import streamlit as st
from streamlit_option_menu import option_menu

from chat.chatbot import chatbot


class Profile:
    def __init__(self, cookies):
        self.cookies = cookies

    def nav_sidebar(self):
        """
        Creates the side navigation bar.
        """
        main_page_sidebar = st.sidebar.empty()
        with main_page_sidebar:
            selected_option = option_menu(
                menu_title="Navigation",
                options=["Profile", "Dashboard", "Chatbot"],
                icons=["person", "speedometer", "chat-dots"],
                menu_icon="list",
                default_index=0,
                styles={
                    "container": {"padding": "5px"},
                    "nav-link": {"font-size": "14px", "text-align": "left", "margin": "0px"}
                }
            )
        return selected_option

    def build_profile_ui(self):
        """
        Builds the profile UI with navigation-like options using Streamlit.
        """
        selected_option = self.nav_sidebar()
        if selected_option == "Profile":
            self.show_profile()
        elif selected_option == "Dashboard":
            self.show_dashboard()
        elif selected_option == "Chatbot":
            self.show_chatbot()

    def show_profile(self):
        """
        Displays the profile page with options to modify user details.
        """
        st.title(f"Welcome, {self.cookies.get('USERNAME')}!")
        st.write("Manage your account details below:")

        profile_pic = st.session_state.get("PROFILE_PIC", None)
        if profile_pic:
            st.image(profile_pic, width=150, caption="Your Profile Picture")
        profile_button = st.button("Modify Profile", key="modify_profile_button")
        if profile_button:
            self.modify_user_data()

        logout_button = st.button("Logout", key="logout_button")
        if logout_button:
            self.logout_user()

    def modify_user_data(self):
        """
        Displays a form to modify user data (name, email, password).
        """
        st.subheader("Modify Your Profile Data")

        with st.form("Modify Profile Form"):
            uploaded_pic = st.file_uploader("Upload a new profile picture:", type=["png", "jpg", "jpeg"])
            if uploaded_pic:
                st.session_state["PROFILE_PIC"] = uploaded_pic
                st.success("Profile picture updated!")
            new_name = st.text_input("New Name", value=st.session_state.get("NAME", ""))
            new_email = st.text_input("New Email", value=st.session_state.get("EMAIL", ""))
            new_password = st.text_input("New Password", type="password", placeholder="Enter new password")

            submit_button = st.form_submit_button("Save Changes")
            if submit_button:
                if new_name:
                    st.session_state["NAME"] = new_name
                if new_email:
                    st.session_state["EMAIL"] = new_email
                if new_password:
                    st.session_state["PASSWORD"] = new_password
                st.success("Profile updated successfully!")
                st.rerun()

    def logout_user(self):
        """
        Logs out the user and clears session state.
        """
        self.cookies["LOGGED_IN"] = "False"
        self.cookies["USERNAME"] = ""
        st.session_state["LOGGED_IN"] = False
        st.session_state["USERNAME"] = None
        st.rerun()

    def show_dashboard(self):
        """
        Displays the dashboard page.
        """
        st.title("Dashboard")
        st.write("This is the dashboard. Display relevant data here.")

    def show_chatbot(self):
        """
        Displays the chatbot page.
        """
        chatbot()

