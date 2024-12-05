import streamlit as st
import requests

user_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user/login'

st.title("Log in into account")
st.sidebar.write("If you're experiencing login issues, please contact us at 787-317-3326.")

with st.form("login"):
    username = st.text_input(label="Username")
    password = st.text_input(label="Password", type="password")
    submit = st.form_submit_button("Login", type='primary')

if submit:
    with st.status("get_account") as status:
        status.update(label="Verifying...", state="running", expanded=False)
        body = {
            "username": username,
            "password": password,
        }

        response = requests.post(user_api, json=body)

        if response.status_code == 200:
            status.update(label="Logging in", state="complete", expanded=False)

            uid = response.json().get("uid", None)
            username = response.json().get("username", None)
            email = response.json().get("email", None)

            st.session_state.uid = uid
            st.session_state.username = username
            st.session_state.email = email

            st.session_state.logged_in = True

            st.rerun()


        else:
            status.update(label="Couldn't log in.", state="error", expanded=True)
            error = response.json().get("error", "Something went wrong. Please try again.")
            st.write(error)

