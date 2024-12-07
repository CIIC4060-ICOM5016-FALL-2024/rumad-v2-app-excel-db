import streamlit as st
import pandas as pd
import requests

room_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room'
general_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db'

def get_data(api_url):
    res_data = requests.get(api_url)
    if res_data.status_code == 200:
        return pd.DataFrame(res_data.json())
    else:
        return None

#get statistics
def post_data(api_url):
    res_data = requests.post(api_url)
    if res_data.status_code == 200:
        return pd.DataFrame(res_data.json())
    else:
        return None

def display_error(message: str):
    c1, c2 = st.columns(2)
    with c1:
        st.header('WOOF!')
        st.subheader(message)
    with c2:
        st.image("img/tarzan.png", width=200)


st.title('Class Statistics :books:')

local_tab, global_tab = st.tabs(["Local", "Global"])


with local_tab:
    stat_c, stat_d = st.tabs(["Top 3 classes that were taught the most per room",
                              "Top 3 most taught classes per semester per year"])
    with stat_c:
        col1, col2 = st.columns(2)
        with col1:
            selected_rid = st.number_input(label= "Please enter a room id", min_value = 0, step = 1, value = 1)
        with col2:
            room_call = room_api + f'/{selected_rid}'
            room = get_data(room_call)

            if room is not None:
                building = room.loc[0, 'building']
                room_number = room.loc[0, 'room_number']
                st.write(f'Room **{room_number}** in the **{building}** building')
            else:
                st.write('A room with that id does not exist')

        stats_call = room_api + f'/{selected_rid}/classes'
        per_room_pd = post_data(stats_call)
        if per_room_pd is not None:
            st.bar_chart(per_room_pd, x="cdesc", y="amount", color="cdesc", horizontal=True)
        else:
            display_error("Couldn't find classes for that room")

    with stat_d:
        col1, col2 = st.columns(2)
        with col1:
            options = ["Fall", "Spring", "First Summer", "Second Summer"]
            selected_term = st.pills(label = "Please select a term", options = options, selection_mode="single", default="Fall")
        with col2:
            selected_year = st.number_input(label="Please enter a year", min_value=0, step=1, value=2017)

        if selected_term == "First Summer":
            selected_term = "v1"
        elif selected_term == "Second Summer":
            selected_term = "v2"

        if selected_term is None:
            display_error("Please select a term")
        else:
            selected_term = selected_term.lower()
            stats_call = general_api + f'/classes/{selected_year}/{selected_term}'
            per_term_per_year_pd = post_data(stats_call)

            if per_term_per_year_pd is not None:
                st.bar_chart(per_term_per_year_pd, x="cdesc", y="section_amount", color="cdesc", horizontal=True)
            else:
                display_error("Couldn't find classes for that term")

with global_tab:
    stat_b, stat_c = st.tabs(["Top 3 classes that appears the most as prerequisite to other classes",
                             "Top 3 classes that were offered the least"])
    with stat_b:
        stat_call = general_api + f'/most/prerequisite'
        most_prerequisite_pd = post_data(stat_call)
        if most_prerequisite_pd is not None:
            st.bar_chart(most_prerequisite_pd, x="cdesc", y="frequency", color="cdesc", horizontal=True)
        else:
            display_error("Couldn't find classes with prerequisites")

    with stat_c:
        stat_call = general_api + f'/least/classes'
        least_pd = post_data(stat_call)
        if least_pd is not None:
            st.bar_chart(least_pd, x="cdesc", y="frequency", color="cdesc", horizontal=True)
        else:
            display_error("Couldn't find any classes")







