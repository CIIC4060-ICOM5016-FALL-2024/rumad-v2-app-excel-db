from re import split

import streamlit as st
import pandas as pd
import requests
import altair as alt

room_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room'
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



st.title('Class Statistics :books:')

local_tab, global_tab = st.tabs(["Local", "Global"])

with st.sidebar:
    st.header("Graph Settings")
    ascending = st.toggle("Ascending")
    order = "descending"
    if ascending:
        order = "ascending"

with local_tab:
    stat_c, stat_d = st.tabs(["Top 3 classes that were taught the most per room",
                              "Top 3 most taught classes per semester per year"])
    with stat_c:
        col1, col2 = st.columns(2)
        with col1:
            rooms = get_data(room_api)
            room_list = []
            for index,row in rooms.iterrows():
                room_list.append(f'{row["rid"]} - {row["building"]} {row["room_number"]}')
            room_tuple = tuple(room_list)
            #selected_rid = st.number_input(label= "Please enter a room id", min_value = 0, step = 1, value = 1)
            selected_rid = st.selectbox("Select room id you would like to see", room_tuple,placeholder="Select room id")
            selected_rid = selected_rid.split(' ')[0]

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
            per_room_pd["cdesc"] = per_room_pd["cname"] + per_room_pd["ccode"]
            bar_chart = (
                alt.Chart(per_room_pd)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "cdesc",axis=alt.Axis(labelAngle=0),
                        title="Class Description",
                        sort=alt.EncodingSortField(field="amount", order=order),
                    ),
                    y=alt.Y("amount:Q", title="Amount"),
                    color=alt.Color("cdesc:N", title="Class Description"),
                )
                .properties(
                    title="Bar Chart by Class Description",
                    width=600,
                    height=400,
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)
            st.write(post_data(stats_call))
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
                per_term_per_year_pd["cdesc"] = per_term_per_year_pd["cname"] + per_term_per_year_pd["ccode"]
                bar_chart = (
                    alt.Chart(per_term_per_year_pd)
                    .mark_bar()
                    .encode(
                        x=alt.X(
                            "cdesc", axis=alt.Axis(labelAngle=0),
                            title="Class Description",
                            sort=alt.EncodingSortField(field="section_amount", order=order),
                        ),
                        y=alt.Y("section_amount", title="Amount"),
                        color=alt.Color("cdesc", title="Class Description"),
                    )
                    .properties(
                        title="Bar Chart by Class Description",
                        width=600,
                        height=400,
                    )
                )
                st.altair_chart(bar_chart, use_container_width=True)
                st.write(post_data(stats_call))
            else:
                display_error("Couldn't find classes for that term")

with global_tab:
    stat_b, stat_c = st.tabs(["Top 3 classes that appears the most as prerequisite to other classes",
                             "Top 3 classes that were offered the least"])
    with stat_b:
        stat_call = general_api + f'/most/prerequisite'
        most_prerequisite_pd = post_data(stat_call)
        if most_prerequisite_pd is not None:
            most_prerequisite_pd["cdesc"] = most_prerequisite_pd["cname"] + most_prerequisite_pd["ccode"]
            bar_chart = (
                alt.Chart(most_prerequisite_pd)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "cdesc", axis=alt.Axis(labelAngle=0),
                        title="Class Description",
                        sort=alt.EncodingSortField(field="frequency", order=order),
                    ),
                    y=alt.Y("frequency", title="Amount"),
                    color=alt.Color("cdesc", title="Class Description"),
                )
                .properties(
                    title="Bar Chart by Class Description",
                    width=600,
                    height=400,
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)
            st.write(post_data(stat_call))
        else:
            display_error("Couldn't find classes with prerequisites")

    with stat_c:
        stat_call = general_api + f'/least/classes'
        least_pd = post_data(stat_call)
        if least_pd is not None:
            least_pd["cdesc"] = least_pd["cname"] + least_pd["ccode"]
            bar_chart = (
                alt.Chart(least_pd)
                .mark_bar()
                .encode(
                    x=alt.X(
                        "cdesc", axis=alt.Axis(labelAngle=0),
                        title="Class Description",
                        sort=alt.EncodingSortField(field="frequency", order=order),
                    ),
                    y=alt.Y("frequency", title="Amount"),
                    color=alt.Color("cdesc", title="Class Description"),
                )
                .properties(
                    title="Bar Chart by Class Description",
                    width=600,
                    height=400,
                )
            )
            st.altair_chart(bar_chart, use_container_width=True)
            st.write(least_pd)
        else:
            display_error("Couldn't find any classes")







