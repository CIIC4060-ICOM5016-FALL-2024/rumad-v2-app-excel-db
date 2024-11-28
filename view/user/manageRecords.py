import datetime
import requests
import pandas as pd
import streamlit as st


class ManageRecords:

    admin_manage = [
        "Create Record",
        "Update Record",
        "Delete Record",
    ]

    # Define tables and their fields
    tables = {
        "login": [
            ("username", str),
            ("password", str),
            ("email", str),
        ],
        "class": [
            ("cname", str),  # Course name
            ("ccode", str),  # Course code
            ("cdesc", str),  # Course description
            ("term", str),  # Term (e.g., Fall, Spring)
            ("years", str),  # Academic years
            ("cred", int),  # Credits
            ("csyllabus", str),  # Syllabus link or reference
        ],
        "meeting": [
            ("ccode", str),  # Related course code
            ("starttime", "time"),  # Start time
            ("endtime", "time"),  # End time
            ("cdays", str),  # Days of the week
        ],
        "requisite": [
            ("classid", "search", "cid", "cname", None),  # Class ID (FK)
            ("reqid", "search", "cid", "cname", None),  # Requisite ID (FK)
            ("prereq", bool),  # Is prerequisite
        ],
        "room": [
            ("building", str),  # Building name
            ("room_number", str),  # Room number
            ("capacity", int),  # Room capacity
        ],
        "section": [
            ("roomid", "search", "rid", "room_number", None),  # Room ID (FK)
            ("cid", "search", "cid", "cname", None),  # Class ID (FK)
            ("mid", "search", "mid", "ccode", None),  # Meeting ID (FK)
            ("semester", str),  # Semester
            ("years", str),  # Academic years
            ("capacity", int),  # Section capacity
        ],
        "syllabus": [
            ("courseid", "search", "cid", "cname", None),  # Course ID (FK)
            ("embedding_text", str),  # Syllabus embedding text
            ("chunk", str),  # Chunk of syllabus
        ],
    }

    # Add all searchable tables
    searchable_content = [
        "login",
        "class",
        "meeting",
        "requisite",
        "room",
        "section",
        "syllabus",
    ]

    def __init__(self):
        self.mainRoute = "https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/"

    def create_as_admin(self):
        st.write("# Manage Records")
        st.subheader("You can create, update, or delete records in here.")
        selected_tab = st.selectbox(
            "Select to manage records", self.admin_manage, index=0
        )

        if selected_tab == "Create Record":
            st.write("# Create Records")
            table_selected = st.selectbox(
                "Select which table to create a new record", self.tables.keys()
            )
            self.create_records(table_selected)
        elif selected_tab == "Update Record":
            self.update_records()
        elif selected_tab == "Delete Record":
            self.delete_records()

    def create_records(self, table_selected):
        if not table_selected:
            return

        result = self.create_widgets(table_selected)
        valid_to_create = result[0]
        fields = result[1]

        if st.button("Create", disabled=not valid_to_create) and valid_to_create:
            response = requests.post(f"{self.mainRoute}{table_selected}", json=fields)
            if response.status_code == 200:
                st.success("Record created successfully!")
            else:
                st.error("Failed to create record, please check your input.")

    def create_widgets(self, table_selected):
        valid_to_create = True
        main_fields = {}

        for column in self.tables[table_selected]:
            column_name = column[0]

            if column[1] == "search":
                # Handle foreign key relationships
                response = requests.get(f"{self.mainRoute}{column_name}")
                options = {
                    record[column[3]]: record[column[2]] for record in response.json()
                }

                selected_option = st.selectbox(f"Select {column_name}", options.keys())
                main_fields[column[2]] = options[selected_option]
            elif column[1] == "time":
                # Handle time fields
                selected_time = st.time_input(f"Select time for {column_name}")
                main_fields[column_name] = selected_time.strftime("%H:%M:%S")
            elif column[1] == bool:
                # Handle boolean fields
                is_checked = st.checkbox(f"{column_name}?")
                main_fields[column_name] = is_checked
            elif column[1] == int:
                # Handle integer fields
                selected_number = st.number_input(f"Enter {column_name}", min_value=0)
                main_fields[column_name] = selected_number
            elif column[1] == str:
                # Handle string fields
                entered_text = st.text_input(f"Enter {column_name}")
                if not entered_text:
                    valid_to_create = False
                main_fields[column_name] = entered_text

        return valid_to_create, main_fields

    def update_records(self):
        st.write("# Update Records")
        table_selected = st.selectbox("Select which table to update", self.searchable_content)
        if not table_selected:
            return

        entity_id = st.number_input(f"Enter ID for {table_selected} record to update", min_value=1)
        
        # Fetch the current record
        if st.button("Fetch Record"):
            response = requests.get(f"{self.mainRoute}{table_selected}/{entity_id}")
            if response.status_code == 200:
                record = response.json()
                st.write("Current Record:", record)

                # Create dynamic update fields
                updated_fields = {}
                for column in self.tables[table_selected]:
                    column_name = column[0]

                    # Check current record values
                    current_value = record.get(column_name, None)

                    if column[1] == "search":
                        response = requests.get(f"{self.mainRoute}{column_name}")
                        options = {record[column[3]]: record[column[2]] for record in response.json()}
                        selected_option = st.selectbox(
                            f"Update {column_name}", options.keys(), index=list(options.values()).index(current_value)
                        )
                        updated_fields[column[2]] = options[selected_option]

                    elif column[1] == "time":
                        # Handle time fields
                        current_time = datetime.datetime.strptime(current_value, "%H:%M:%S").time()
                        selected_time = st.time_input(f"Update {column_name}", current_time)
                        updated_fields[column_name] = selected_time.strftime("%H:%M:%S")

                    elif column[1] == bool:
                        # Handle boolean fields
                        is_checked = st.checkbox(f"{column_name}?", value=current_value)
                        updated_fields[column_name] = is_checked

                    elif column[1] == int:
                        # Handle integer fields
                        selected_number = st.number_input(f"Update {column_name}", value=current_value, min_value=0)
                        updated_fields[column_name] = selected_number

                    elif column[1] == str:
                        # Handle string fields
                        entered_text = st.text_input(f"Update {column_name}", value=current_value)
                        updated_fields[column_name] = entered_text

                    elif column[1] == float:
                        # Handle float fields
                        selected_float = st.number_input(f"Update {column_name}", value=current_value, format="%.2f")
                        updated_fields[column_name] = selected_float

                # Submit updated fields
                if st.button("Update Record"):
                    update_response = requests.put(f"{self.mainRoute}{table_selected}/{entity_id}", json=updated_fields)
                    if update_response.status_code == 200:
                        st.success("Record updated successfully!")
                    else:
                        st.error("Failed to update record, please check your input.")
            else:
                st.error("Failed to fetch the record. Ensure the ID is correct.")

    def delete_records(self):
        st.write("# Delete Records")
        table_selected = st.selectbox("Select which table to delete from", self.searchable_content)
        if not table_selected:
            return

        entity_id = st.number_input(f"Enter ID for the {table_selected} record to delete", min_value=1)
        if st.button("Delete Record"):
            response = requests.delete(f"{self.mainRoute}{table_selected}/{entity_id}")
            if response.status_code == 200:
                st.success(f"Record deleted successfully from {table_selected}!")
            elif response.status_code == 404:
                st.error("Record not found. Please check the ID.")
            elif response.status_code == 400:
                st.error("This record is referenced by other tables. Remove related records first.")
            else:
                st.error("Failed to delete record. Please check your input and try again.")