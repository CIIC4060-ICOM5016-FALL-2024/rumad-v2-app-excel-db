import datetime
import requests
import streamlit as st


class ManageRecords:

    admin_manage = [
        "Create Record",
        "Update Record",
        "Delete Record",
        "Get Record",  # New Option Added
    ]

    # Define tables and their fields
    tables = {
        "users": [
            ("username", str),
            ("password", str),
            ("email", str),
        ],
        "class": [
            ("cname", str),
            (
                "ccode",
                ["CIIC", "INSO", "Authorization for the Director of the Department"],
            ),
            ("cdesc", str),
            (
                "term",
                [
                    "First Semester",
                    "Second Semester",
                    "First Semester, Second Semester",
                    "According to Demand",
                ],
            ),
            ("years", ["Every Year", "Even Years", "Odd Years", "According to"]),
            ("cred", int),
            ("csyllabus", str),
        ],
        "meeting": [
            ("ccode", str),
            ("starttime", "time"),
            ("endtime", "time"),
            ("cdays", ["LWV", "MJ"]),
        ],
        "requisite": [
            ("classid", int),  # CHECK THIS!!!
            ("reqid", int),
            ("prereq", bool),
        ],
        "room": [
            ("building", str),
            ("room_number", str),
            ("capacity", int),
        ],
        "section": [
            ("sid", int),
            ("roomid", "search", "rid", "room_number", None),
            ("cid", "search", "cid", "cname", None),
            ("mid", "search", "mid", "ccode", None),
            ("semester", str),
            ("years", str),
            ("capacity", int),
        ],
        "syllabus": [
            ("courseid", "search", "cid", "cname", None),
            ("embedding_text", str),
            ("chunk", str),
        ],
    }

    # Searchable tables for Update and Delete
    searchable_content = list(tables.keys())

    def __init__(self):
        self.mainRoute = (
            "https://rumad-v2-app-excel-db-881d3c171d54.herokuapp.com/excel_db/"
        )

    def create_as_admin(self):
        st.title("Manage Records")
        st.subheader("Create, Update, Delete, or Retrieve Records")
        selected_tab = st.selectbox("Select Operation", self.admin_manage)

        if selected_tab == "Create Record":
            self.handle_create()
        elif selected_tab == "Update Record":
            self.handle_update()
        elif selected_tab == "Delete Record":
            self.handle_delete()
        elif selected_tab == "Get Record":
            self.handle_get()

    def handle_create(self):
        """
        Handles the Create Record operation.
        Prompts the user to select a table and generates a form for creating a new record.
        """
        st.header("Create Record")
        table_selected = st.selectbox("Select Table", self.tables.keys())
        if table_selected:
            self.create_record(table_selected)

    # def create_record(self, table_selected):
    #     """
    #     Generates a form for creating a record in the specified table.
    #     Submits the form data to the API as a POST request.
    #     """

    #     st.header("Create Record")
    #     table_selected = st.selectbox("Select Table", self.tables.keys())
    #     if table_selected:
    #         self.create_record(table_selected)

    #     valid, fields = self.generate_form(table_selected)
    #     if st.button("Create Record", disabled=not valid):
    #         response = requests.post(f"{self.mainRoute}{table_selected}", json=fields)
    #         if response.status_code == 200:
    #             st.success("Record created successfully!")
    #         else:
    #             st.error("Failed to create record. Please check your input.")

    def create_record(self, table_selected):
        st.header(f"Create Record in {table_selected}")

        # Generate form fields dynamically
        valid, fields = self.generate_form(table_selected)

        if not valid:
            st.error("All fields are required for this operation.")

        # Display a button to create the record
        if st.button("Create Record", disabled=not valid):
            response = requests.post(f"{self.mainRoute}{table_selected}", json=fields)
            if response.status_code == 201:
                st.success(f"Record successfully created in {table_selected}!")
            else:
                st.error(f"Failed to create record in {table_selected}. Please check your input.")



    def handle_update(self):
        """
        Handles the Update Record operation.
        Prompts the user to select a table and fetches an existing record by ID for editing.
        """
        st.header("Update Record")

        table_selected = st.selectbox("Select Table to Update", self.searchable_content)
        if table_selected:
            if table_selected == "users":
                # Use username for users table
                username = st.text_input(f"Enter username for {table_selected}")
                if st.button("Fetch Record"):
                    response = requests.get(f"{self.mainRoute}/user/{username}")
                    if response.status_code == 200 and response.json():
                        record = response.json()
                        self.update_record(table_selected, record['id'], record)  
                    else:
                        st.error("Failed to fetch record. Ensure the username is correct.")
            else:
                entity_id = st.number_input(f"Enter ID for {table_selected}", min_value=1)
                if st.button("Fetch Record"):
                    response = requests.get(f"{self.mainRoute}{table_selected}/{entity_id}")
                    if response.status_code == 200:
                        record = response.json()
                        self.update_record(table_selected, entity_id, record)
                    else:
                        st.error("Failed to fetch record. Ensure the ID is correct.")


    def update_record(self, table_selected, entity_id, record):
        """
        Generates a form for updating an existing record.
        Submits the updated data to the API as a PUT request.
        """

        st.header(f"Update Record in {table_selected}")

        st.write("Current Record:", record)

        valid, updated_fields = self.generate_form(table_selected, record)

        if not valid:
            st.error("All fields are required for this operation.")

        if st.button("Update Record", disabled=not valid):
            response = requests.put(f"{self.mainRoute}{table_selected}/{entity_id}", json=updated_fields)
            if response.status_code == 200:
                st.success(f"Record successfully updated in {table_selected}!")
            else:
                st.error(f"Failed to update record in {table_selected}. Please check your input.")

    def handle_delete(self):
        """
        Handles the Delete Record operation.
        Prompts the user to select a table and delete a record by ID.
        """
        st.header("Delete Record")

        table_selected = st.selectbox("Select Table to Delete From", self.searchable_content)
        if table_selected:
            entity_id = st.number_input(f"Enter ID for {table_selected}", min_value=1)
            valid, fields = self.generate_form(table_selected)  # Ensure all fields are filled

            if not valid:
                st.error("All fields are required for this operation.")

            # Delete the record only if valid
            if st.button("Delete Record", disabled=not valid):
                response = requests.delete(f"{self.mainRoute}{table_selected}/{entity_id}")
                if response.status_code == 200:
                    st.success("Record successfully deleted!")
                else:
                    st.error("Failed to delete record. Ensure the ID and input are correct.")


    def handle_get(self):
        """
        Handles the Get Record operation.
        Prompts the user to select a table and fetch a record by ID.
        """
        st.header("Get Record")

        table_selected = st.selectbox("Select Table to Fetch From", self.searchable_content)
        if table_selected:
            if table_selected == "users":
                username = st.text_input(f"Enter username for {table_selected}")
                if st.button("Fetch Record"):
                    response = requests.get(f"{self.mainRoute}/user/{username}")
                    if response.status_code == 200 and response.json():
                        st.write("Fetched Record:", response.json())
                    else:
                        st.error("Failed to fetch record. Ensure the username is correct.")
            else:
                entity_id = st.number_input(f"Enter ID for {table_selected}", min_value=1)
                if st.button("Fetch Record"):
                    response = requests.get(f"{self.mainRoute}{table_selected}/{entity_id}")
                    if response.status_code == 200:
                        st.write("Fetched Record:", response.json())
                    else:
                        st.error("Failed to fetch record. Ensure the ID is correct.")



    def generate_form(self, table_selected, record=None):
        """
        Dynamically generate form fields based on table schema with strict validation.
        """
        valid = True
        fields = {}

        for column in self.tables[table_selected]:
            column_name = column[0]
            column_type = column[1]
            current_value = record.get(column_name, None) if record else None

            if column_name == "username" and table_selected == "users":
                entered_text = st.text_input(f"{column_name}", value=current_value or "", key=f"{column_name}_str")
                if not entered_text:
                    valid = False
                fields[column_name] = entered_text

            elif column_type == "search":
                response = requests.get(f"{self.mainRoute}{column_name}")
                options = {rec[column[3]]: rec[column[2]] for rec in response.json()}
                selected_option = st.selectbox(
                    f"{column_name}",
                    options.keys(),
                    index=0 if current_value is None else list(options.values()).index(current_value),
                    key=f"{column_name}_search"
                )
                fields[column[2]] = options[selected_option]

            elif column_type == "time":
                time_value = datetime.datetime.strptime(current_value, "%H:%M:%S").time() if current_value else datetime.time(0, 0)
                selected_time = st.time_input(f"{column_name}", time_value, key=f"{column_name}_time")
                fields[column_name] = selected_time.strftime("%H:%M:%S")

            elif type(column_type) == list:
                selected_value = st.selectbox(
                    f"{column_name}",
                    column_type,
                    index=0 if current_value is None else column_type.index(current_value),
                    key=f"{column_name}_list"
                )
                fields[column_name] = selected_value

            elif column_type == str:
                entered_text = st.text_input(f"{column_name}", value=current_value or "", key=f"{column_name}_str")
                if not entered_text:
                    valid = False
                fields[column_name] = entered_text

            elif column_type == int:
                entered_number = st.number_input(f"{column_name}", value=current_value or 0, min_value=0, key=f"{column_name}_int")
                fields[column_name] = entered_number

            elif column_type == bool:
                is_checked = st.checkbox(f"{column_name}", value=current_value or False, key=f"{column_name}_bool")
                fields[column_name] = is_checked

        return valid, fields
