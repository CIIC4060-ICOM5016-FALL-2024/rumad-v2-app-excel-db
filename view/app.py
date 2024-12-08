import streamlit as st

if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False

pages = {}
if st.session_state.logged_in:
    home_page = st.Page("pages/dashboard.py", title="Dashboard")
    account_page = st.Page("pages/account.py", title="Account")
    class_page = st.Page("pages/class.py", title="Classes")
    sections_page = st.Page("pages/section.py", title="Sections")
    meeting_page = st.Page("pages/meeting.py", title="Meetings")
    room_page = st.Page("pages/room.py", title="Rooms")
    pages = {"Home": [home_page, account_page],
             "Statistics": [class_page, sections_page, meeting_page, room_page]}
else:
    login_page = st.Page("pages/login.py", title="Login")
    register_page = st.Page("pages/register.py", title="Register")
    pages = {"Account": [register_page, login_page]}



pg = st.navigation(pages)

st.set_page_config(page_title="RUMAD 2.0",
                   page_icon="img/sello_uprm.svg",
                   layout="wide",
                )
st.logo('img/uprm_web_logo.png', icon_image='img/sello_uprm.svg')
st.sidebar.title("RUMAD 2.0")


pg.run()

