import streamlit as st
import pandas as pd
import requests


def dashboard():
    def classes_per_semester(year, semester):
        try:
            response = requests.post(
                f"https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/classes/{year}/{semester}")
            if response.status_code != 200:
                return "Data for this term does not exist"
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            print(f"An error occurred: {e}")

    def get_all_rooms():
        try:
            response = requests.get("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def display_sections_per_year():
        try:
            response = requests.post("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/section/year")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def display_least_offered_classes():
        try:
            response = requests.post("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/least/classes")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def display_top_prerequisite():
        try:
            response = requests.post(
                "https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/most/prerequisite")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def display_top_5_meetings():
        try:
            response = requests.post("https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/most/meeting")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def top_rooms_per_building(building):
        try:
            response = requests.post(
                f"https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room/{building}/capacity")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def top_ratio_per_building(building):
        try:
            response = requests.post(
                f"https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room/{building}/ratio")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    def classes_taught_most_per_room(room):
        try:
            response = requests.post(
                f"https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room/{room}/classes")
            response.raise_for_status()
            result = response.json()
            pd_result = pd.DataFrame(result)
            return pd_result
        except requests.RequestException as e:
            return f"An error occurred: {e}"

    st.title("Metrics Dashboard")
    st.subheader("This page contains information on statistics for classes individually and globally")
    options = ("Total number of sections per year", "Top 3 classes that were offered the least",
               "Top 3 classes that appears the most as prerequisite to other classes",
               "Top 5 meetings with the most sections")

    selected = st.selectbox("Select the global statistic that you would like to see.",
                            options, placeholder="Select an statistic to show")

    if selected == "Total number of sections per year":
        data = display_sections_per_year()
        col1, col2 = st.columns(2)
        with col1:
            chart_type = st.radio("Select the type of graph to display", ["Line Chart", "Bar chart", "Scatter Chart"], )
        if isinstance(data, pd.DataFrame):
            with col2:
                if chart_type == "Line Chart":
                    st.line_chart(data, x='year',
                                  y='total_sections',
                                  x_label='Year',
                                  y_label='Number of sections')
                if chart_type == "Bar chart":
                    st.bar_chart(data, x='year',
                                 y='total_sections',
                                 x_label='Year',
                                 y_label='Number of sections')
                if chart_type == "Scatter Chart":
                    st.scatter_chart(data, x='year',
                                     y='total_sections',
                                     x_label='Year',
                                     y_label='Number of sections')
        else:
            with col2:
                st.write(data)

    if selected == "Top 3 classes that were offered the least":
        data = display_least_offered_classes()
        if isinstance(data, pd.DataFrame):
            data = data.sort_values(by='frequency', ascending=False)
            st.bar_chart(data, x='cdesc',
                         y='frequency',
                         x_label='Amount of times offered',
                         y_label='Class',
                         width=500,
                         height=500)
        else:
            st.write(data)

    if selected == "Top 3 classes that appears the most as prerequisite to other classes":
        data = display_top_prerequisite()
        if isinstance(data, pd.DataFrame):
            data = data.sort_values(by='frequency', ascending=False)
            st.bar_chart(data,
                         x="cdesc",
                         y="frequency",
                         y_label='Total amount of prerequisites',
                         x_label='Class name ( None: Authorization from the Director of the Department)')
            st.write(data)

    if selected == "Top 5 meetings with the most sections":
        data = display_top_5_meetings()
        if isinstance(data, pd.DataFrame):
            data = data.sort_values(by='frequency', ascending=False)
            st.bar_chart(data, x="mid"
                             , y="frequency",
                             x_label='Meeting ID',
                             y_label='Number of Sections')
            second_data = data.drop(columns=['frequency', 'ccode'])
            st.table(second_data)
        else:
            st.write(data)

    options = ("Top 3 rooms per building with the most capacity",
               "Top 3 room with the most student-to-capacity ratio",
               "Top 3 classes that were taught the most per room",
               "Top 3 most taught classes per semester per year")

    selected = st.selectbox("Select the local statistics that you would like to see.",
                            options, placeholder="Select an statistic to show")

    if selected == "Top 3 rooms per building with the most capacity":
        col1, col2 = st.columns(2)
        building_list = get_all_rooms()
        if isinstance(building_list, pd.DataFrame):
            building_list = building_list["building"].values.tolist()
            building_list = list(dict.fromkeys(building_list))
            with col1:
                building = st.radio("Choose the building you would like to see.", building_list)
                data = top_rooms_per_building(building)
                if isinstance(data, pd.DataFrame):
                    data = data.sort_values(by='room_number', ascending=False)
                    with col2:
                        st.bar_chart(data, x='room_number',
                                     y='capacity',
                                     x_label='Room Number',
                                     y_label='Capacity',
                                     width=500, height=500)
                else:
                    st.write(data)
        else:
            st.write(building_list)

    if selected == "Top 3 room with the most student-to-capacity ratio":
        col1, col2 = st.columns(2)
        building_list = get_all_rooms()
        if isinstance(building_list, pd.DataFrame):
            building_list = building_list["building"].values.tolist()
            building_list = list(dict.fromkeys(building_list))

            with col1:
                building = st.radio("Choose the building you would like to see.", building_list)
                data = top_ratio_per_building(building)
                if isinstance(data, pd.DataFrame):
                    data = data.sort_values(by='ratio', ascending=False)
                    with col2:
                        st.bar_chart(data, x='room_number', y='ratio',
                                     x_label='Room Number',
                                     y_label='Ratio',
                                     width=500, height=500)
                else:
                    st.write(data)
        else:
            st.write(building_list)

        if isinstance(data, pd.DataFrame):
            st.table(data)

    if selected == "Top 3 classes that were taught the most per room":

        input = st.text_input("Input room id", placeholder="Room id #")
        room_data = get_all_rooms()
        if isinstance(room_data, pd.DataFrame):
            room_data = room_data.drop(columns=['capacity'])
            rid_list = [str(x) for x in room_data["rid"].values.tolist()]
            if input not in rid_list:
                st.write("Please enter a valid room id")
            else:
                selected_room_data = room_data[room_data['rid'] == int(input)]
                rid = selected_room_data['rid'].values[0]
                building = selected_room_data['building'].values[0]
                room_number = selected_room_data['room_number'].values[0]

                st.write(f"Room with rid {rid} corresponds to room {room_number} in the {building} building.")

                data = classes_taught_most_per_room(input)
                if isinstance(data, pd.DataFrame):
                    data = data.sort_values(by='amount', ascending=False)
                    st.bar_chart(data, x='cdesc',
                                 y='amount',
                                 x_label="Class",
                                 y_label="Amount taught",
                                 width=500, height=500)
                else:
                    st.write(data)
        else:
            st.write(room_data)

    if selected == "Top 3 most taught classes per semester per year":
        col1, col2 = st.columns(2)
        years = display_sections_per_year()
        if isinstance(years, pd.DataFrame):
            years = years["year"].values.tolist()
            min_year = int(min(years))
            max_year = int(max(years))

            with col1:
                input = st.slider("Choose the year you would like to see.", min_value=min_year, max_value=max_year, step=1)
                term = st.selectbox("Choose the semester", ("Spring", "Fall", "V1", "V2"))
            with col2:
                data = classes_per_semester(input, term)
                if isinstance(data, pd.DataFrame):
                    data = data.sort_values(by='section_amount', ascending=False)
                    st.bar_chart(data, x='cdesc',
                                     y='section_amount',
                                     x_label="Section Amount",
                                     y_label="Class", width=500,
                                     height=500)
                else:
                    st.write(data)
        else:
            st.write(years)
