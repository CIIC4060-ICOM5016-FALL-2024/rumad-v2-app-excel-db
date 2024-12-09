import streamlit as st
import pandas as pd
import requests
import altair as alt

import matplotlib.pyplot as plt

room_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room'


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


def get_all_buildings(api_url):
    """
    Gets all buildings from the api url
    @param api_url: api endpoint
    @return: A dataframe or None
    """
    try:
        res_data = requests.get(api_url)
        if res_data.status_code == 200:
            df = pd.DataFrame(res_data.json())
            buildings = df['building'].unique()
            return buildings
        else:
            return None
    except Exception:
        return None


st.title('Room Statistics :school:')

tabs = st.tabs(["Local"])
local_tab = tabs[0]

with st.sidebar:
    st.header("Graph Settings")
    ascending = st.toggle("Ascending")
    order = "descending"
    if ascending:
        order = "ascending"

with local_tab:
    stat_a, stat_b = st.tabs(
        ["Top 3 rooms per building with the most capacity", "Top 3 room with the most student-to-capacity ratio"])
    with stat_a:
        buildings = get_all_buildings(room_api)
        if buildings is not None:
            selected_building = st.pills(label="Please select a building", options=buildings, selection_mode="single",
                                         default='Stefani', key="stata")
            if selected_building is not None:
                stat_call = room_api + f'/{selected_building}/capacity'
                rooms_w_most_capacity_pd = post_data(stat_call)
                if rooms_w_most_capacity_pd is not None:
                    rooms_w_most_capacity_pd['rid'] = rooms_w_most_capacity_pd["building"] + "-" + rooms_w_most_capacity_pd["room_number"] 
                    bar_chart = (
                        alt.Chart(rooms_w_most_capacity_pd)
                        .mark_bar()
                        .encode(
                            x=alt.X(
                                "rid",axis=alt.Axis(labelAngle=0),
                                title="Class Room",
                                type="nominal",
                                sort=alt.EncodingSortField(field="capacity", order=order),
                            ),
                            y=alt.Y("capacity", title="Capacity")
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
                    display_error("No rooms found")
            else:
                display_error("Please select a building")
        else:
            display_error("No buildings found")
    with stat_b:
        buildings = get_all_buildings(room_api)
        if buildings is not None:
            selected_building = st.pills(label="Please, select a building", options=buildings, default="Stefani",
                                         key="statb")
            if selected_building is not None:
                stat_call = room_api + f'/{selected_building}/ratio'
                rooms_w_most_capacity_pd = post_data(stat_call)
                if rooms_w_most_capacity_pd is not None and not rooms_w_most_capacity_pd.empty:
                    # Dynamically handle up to 3 rooms
                    cols = st.columns(min(3, len(rooms_w_most_capacity_pd)))

                    for idx, (room_id, row) in enumerate(rooms_w_most_capacity_pd.iterrows()):
                        if idx >= 3:
                            break
                        with cols[idx]:
                            st.write(f"Room {row['room_number']} in {row['building']}")
                            # Data for the pie chart
                            capacity = row['capacity']
                            students = row['ratio'] / 100 * capacity
                            available_seats = capacity - students

                            # Pie chart visualization
                            fig, ax = plt.subplots()
                            ax.pie(
                                [students, available_seats],
                                labels=["Students", "Free seats"],
                                autopct='%1.1f%%',
                                startangle=90
                            )
                            ax.axis('equal')  # Equal aspect ensures a circular pie chart.
                            st.pyplot(fig)
                            st.write(rooms_w_most_capacity_pd)
                else:
                    display_error("No rooms found")
            else:
                display_error("Please select a building")
        else:
            display_error("No buildings found")