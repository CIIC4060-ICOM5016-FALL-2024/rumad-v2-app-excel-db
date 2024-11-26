import streamlit as st
import time

from streamlit_cookies_manager import EncryptedCookieManager
from user.login import Login
from user.profile import Profile

def main():
    cookies = EncryptedCookieManager(password="admin")
    while not cookies.ready():
        time.sleep(0.1)

    profile_page = Profile(cookies)
    login_page = Login(cookies)
    if cookies.get("LOGGED_IN") == "True":
        profile_page.build_profile_ui()
    else:
        if login_page.build_login_ui():
            cookies["LOGGED_IN"] = "True"
            cookies["USERNAME"] = login_page.get_username()
            st.session_state["LOGGED_IN"] = True
            st.session_state["USERNAME"] = login_page.get_username()
            st.stop()



if __name__ == "__main__":
    st.set_page_config(page_title="Excel", page_icon="🤖", layout="centered", initial_sidebar_state="auto")
    main()
