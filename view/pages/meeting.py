import streamlit as st
import pandas as pd
import requests

general_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db'

def get_data(api_url):
    """
    Gets a dataframe from the api url
    @param api_url: URL of the api endpoint
    @return: A dataframe or None
    """
    try:
        res_data = requests.get(api_url)
        if res_data.status_code == 200:
            return pd.DataFrame(res_data.json())
        else:
            return None
    except Exception:
        return None


#get statistics
def post_data(api_url):
    """
    Gets a dataframe from the api url. This work for statistics.
    @param api_url: URL of the api endpoint
    @return: A dataframe or None
    """
    try:
        res_data = requests.post(api_url)
        if res_data.status_code == 200:
            return pd.DataFrame(res_data.json())
        else:
            return None
    except Exception:
        return None

def display_error(message: str):
    """
    Displays a friendly error message
    @param message: a message to display
    """
    c1, c2 = st.columns(2)
    with c1:
        st.header('WOOF!')
        st.subheader(message)
    with c2:
        st.image("img/tarzan.png", width=200)



st.title('Meeting Statistics :calendar:')

tabs = st.tabs(["Global"])
global_tab = tabs[0]  # Access the first tab

# Work within the global tab
with global_tab:
    sub_tabs = st.tabs(["Top 5 meetings with the most sections"])
    sub_tab = sub_tabs[0]
    with sub_tab:
        stat_call = general_api + f'/most/meeting'
        meetings_w_most_sections_pd = post_data(stat_call)
        if meetings_w_most_sections_pd is not None:
            st.bar_chart(meetings_w_most_sections_pd, x="mid", y="frequency", y_label="Sections", color="mid")
        else:
            display_error("No meetings found")