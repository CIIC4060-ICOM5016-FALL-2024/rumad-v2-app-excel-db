import streamlit as st
import requests

user_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user'

st.sidebar.write("RUMAD is the backend platform that manages data services for handling "
         "student enrollment, internal administrative services, and any programs "
         "operated by the Center for Information Technologies (CTI) or other departments "
         "within the campus.")

st.title("Create an account")

with st.form("register"):
    username = st.text_input(label="Username")
    email = st.text_input(label="Email *(upr.edu)*", placeholder="@upr.edu")
    password = st.text_input(label="Password", type="password")
    confirm_password = st.text_input(label="Confirm Password", type="password")
    submit = st.form_submit_button("Create account", type='primary')

if submit:
    if password != confirm_password:
        st.error("Passwords do not match. Please try again.")
    else:
        with st.status("post_account") as status:
            status.update(label="Creating account...", state="running", expanded=False)
            body = {
                "username": username,
                "email": email,
                "password": password,
            }

            response = requests.post(user_api, json=body)

            if response.status_code == 201:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.email = email
                status.update(label="Registered!", state="complete", expanded=False)
                st.rerun()

            else:
                status.update(label="Couldn't create account", state="error", expanded=True)
                error = response.json().get("error", "Something went wrong. Please try again.")
                st.write(error)





