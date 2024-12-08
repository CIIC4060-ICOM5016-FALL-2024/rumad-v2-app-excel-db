import streamlit as st
import pandas as pd
import requests

class_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/class'
requisite_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/requisite'
section_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/section'
meeting_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/meeting'
room_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/room'
user_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/user'


if 'uid' not in st.session_state:
    res = requests.get(user_api + f'/{st.session_state.username}')
    if res.status_code == 200:
        st.session_state.uid = res.json()[0].get("uid", None)
    else:
        st.toast("Couldn't find user id")

def get_data(api_url):
    try:
        res_data = requests.get(api_url)
        if res_data.status_code == 200:
            return pd.DataFrame(res_data.json())
        else:
            return None
    except Exception:
        return None

# Fetch data
class_pd = get_data(class_api)
requisite_pd = get_data(requisite_api)
sections_pd = get_data(section_api)
meeting_pd = get_data(meeting_api)
room_pd = get_data(room_api)

# Create a dictionary to store entity names and data
entities = {
    "Classes :books:": class_pd,
    "Requisites :clipboard:": requisite_pd,
    "Sections :male-teacher:": sections_pd,
    "Meetings :calendar:": meeting_pd,
    "Rooms :school:": room_pd,
}


st.title(f'Welcome, {st.session_state.username}!')
st.subheader('Dashboard')

# Display data in a 3x3 grid
cols_per_row = 3
entity_list = list(entities.items())

# Create rows
for i in range(0, len(entity_list), cols_per_row):
    row = st.columns(cols_per_row)
    for col, (entity, data) in zip(row, entity_list[i:i + cols_per_row]):
        with col.container(border=True):
            st.subheader(entity)
            st.title(data.shape[0] if data is not None else "No Data")

# Mapping dictionary for display names (without emojis)
entity_mapping = {
    "Classes :books:": "Classes",
    "Requisites :clipboard:": "Requisites",
    "Sections :male-teacher:": "Sections",
    "Meetings :calendar:": "Meetings",
    "Rooms :school:": "Rooms",
}

dropdown_options = [entity_mapping[key] for key in entities.keys()]

# Dropdown for selecting entity
selected_display_name = st.selectbox("Select an entity to view details:", options=dropdown_options)

selected_entity = next(key for key, value in entity_mapping.items() if value == selected_display_name)

# Display table for the selected entity
if selected_entity:
    st.write(f"### {selected_entity} Details")
    data = entities[selected_entity]
    if data is not None and not data.empty:
        reordered_data = data[list(data.columns)]  # Preserve the current order
        st.dataframe(reordered_data) 
    else:
        st.warning("No data available for the selected entity.")