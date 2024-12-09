import streamlit as st
import requests
from aiohttp import payload

user_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user'

st.subheader("Account Details")

col1, col2 = st.columns(2)

with col1:
    st.write("Your account info")
    st.image("img/tarzan.png", width=300)
with col2:
    with st.form(key="account_form"):
        st.write("Your ID: ", st.session_state.uid)
        username = st.text_input(label="username", value=st.session_state.username)
        email = st.text_input(label="email", value=st.session_state.email)
        password = st.text_input(label="password", type="password", disabled=True)
        
        update_button = st.form_submit_button(label="Update Account")
        logout_button = st.form_submit_button(label="Logout")
        
        if update_button:
                with st.status("update_account") as status:
                    status.update(label="Updating...", state="running", expanded=False)
                    body = {}
                    if username:
                        body['username'] = username
                    if email:
                        body['email'] = email
                    if password:
                        body['password'] = password
                    response = requests.put(user_api + f"/{st.session_state.uid}", json=body)
                    if response.status_code == 200:
                        if username:
                            st.session_state.username = username
                        if email:
                            st.session_state.email = email
                        status.update(label="Account Updated", state="complete", expanded=False)
                    else:
                        status.update(label="Couldn't update account", state="error", expanded=True)
                        st.write(response.json())

        if logout_button:
            for key in st.session_state.keys():
                del st.session_state[key]
            st.success("Logged out successfully!")
            st.rerun()


st.divider()


@st.dialog("Delete Account")
def delete_account():
    st.subheader("Are you sure you want to delete this account?")
    confirm = st.button(label="Delete this account", type="primary")
    if confirm:
        delete_response = requests.delete(user_api + f"/{st.session_state.uid}")
        if delete_response.status_code == 200:
            # Delete all the items in Session state
            for key in st.session_state.keys():
                del st.session_state[key]
            st.success("Deleted account")
            st.rerun()
        else:
            st.error("Couldn't delete account")


delete = st.button(label="Delete Account", type="primary")
if delete:
    delete_account()



