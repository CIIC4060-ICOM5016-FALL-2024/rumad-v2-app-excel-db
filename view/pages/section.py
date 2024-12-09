import streamlit as st
import pandas as pd
import requests
import altair as alt

general_api = 'https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db'

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


st.title('Section Statistics :male-teacher:')

tabs = st.tabs(["Global"])
global_tab = tabs[0]  # Access the first tab

# Work within the global tab
with global_tab:
    sub_tabs = st.tabs(["Total number of sections per year"])
    sub_tab = sub_tabs[0]
    with sub_tab:
        stat_call = general_api + f'/section/year'
        sections_per_year = post_data(stat_call)
        if sections_per_year is not None:
            line_chart = alt.Chart(sections_per_year).mark_line(strokeWidth=5).encode(
                x=alt.X('year:O', title='Year', axis=alt.Axis(labelAngle=0)),  # Horizontal labels
                y=alt.Y('total_sections:Q', title='Sections'),
                ).properties(
                    title={
                        'text':f'Total Number of Sections per Year',
                        'align': 'center',
                        'anchor': 'middle',
                        'fontSize': 30
                    },
                    width=600,
                    height=400
                )

            # Display the chart and the DataFrame
            st.altair_chart(line_chart, use_container_width=True) 
            st.write(sections_per_year)
        else:
            display_error("No sections found")
            