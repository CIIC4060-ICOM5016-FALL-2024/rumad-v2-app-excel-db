from sqlalchemy import create_engine, Integer, String, DateTime, text
import pandas as pd
from ETL.extract_data import (
    get_sections,
    get_meetings,
    get_rooms,
    get_courses,
    get_requisites,
)
from ETL.transform_data import transform_data
import os
import requests


def create_db(engine):
    sql_commands = """
        CREATE TABLE class (
            cid       SERIAL PRIMARY KEY,
            cname     VARCHAR,
            ccode     VARCHAR,
            cdesc     VARCHAR,
            term      VARCHAR,
            years     VARCHAR,
            cred      INTEGER,
            csyllabus VARCHAR
        );

        ALTER TABLE class OWNER TO excel;

        CREATE TABLE meeting (
            mid       SERIAL PRIMARY KEY,
            ccode     VARCHAR,
            starttime TIMESTAMP,
            endtime   TIMESTAMP,
            cdays     VARCHAR
        );

        ALTER TABLE meeting OWNER TO excel;

        CREATE TABLE requisite (
            classid INTEGER NOT NULL REFERENCES class(cid),
            reqid   INTEGER NOT NULL REFERENCES class(cid),
            prereq  BOOLEAN,
            PRIMARY KEY (classid, reqid)
        );

        ALTER TABLE requisite OWNER TO excel;

        CREATE TABLE room (
            rid         SERIAL PRIMARY KEY,
            building    VARCHAR,
            room_number VARCHAR,
            capacity    INTEGER
        );

        ALTER TABLE room OWNER TO excel;

        CREATE TABLE section (
            sid      SERIAL PRIMARY KEY,
            roomid   INTEGER REFERENCES room(rid),
            cid      INTEGER REFERENCES class(cid),
            mid      INTEGER REFERENCES meeting(mid),
            semester VARCHAR,
            years    VARCHAR,
            capacity INTEGER
        );

        ALTER TABLE section OWNER TO excel;

        CREATE TABLE syllabus (
            chunkid        SERIAL PRIMARY KEY,
            courseid       INTEGER REFERENCES class(cid),
            embedding_text INT2VECTOR,
            chunk          VARCHAR
        );

        ALTER TABLE syllabus OWNER TO excel;
    """

    # Connect to the database and execute SQL
    try:
        with engine.connect() as connection:
            with connection.begin():  # Use a transaction
                connection.execute(
                    text(sql_commands)
                )  # Use text() for raw SQL commands
            print("Tables created successfully.")
    except Exception as e:
        print(f"Error: {e}")  # Print the actual error message


def load_classes(courses, engine):
    courses["cred"] = pd.to_numeric(courses["cred"], errors="coerce")
    courses["cred"] = courses["cred"].fillna(0)
    courses.rename(
        columns={
            "classid": "cid",
            "name": "cname",
            "code": "ccode",
            "description": "cdesc",
            "syllabus": "csyllabus",
        },
        inplace=True,
    )
    # Fetch existing cids from the database
    existing_cids = pd.read_sql_query("SELECT cid FROM class", engine)["cid"].tolist()

    # Filter out rows from courses that have duplicate cid
    courses_to_insert = courses[~courses["cid"].isin(existing_cids)]
    courses_to_insert.to_sql(
        "class",
        engine,
        if_exists="append",
        index=False,
        dtype={
            "cid": Integer(),
            "cname": String(),
            "ccode": String(),
            "cdesc": String(),
            "term": String(),
            "years": String(),
            "cred": Integer(),
            "csyllabus": String(),
        },
    )


def load_meeting(meetings, engine):
    meetings["start"] = pd.to_datetime(meetings["start"])
    meetings["end"] = pd.to_datetime(meetings["end"])
    meetings.rename(
        columns={"start": "starttime", "end": "endtime", "day": "cdays"}, inplace=True
    )

    existing_mids = pd.read_sql_query("SELECT mid FROM meeting", engine)["mid"].tolist()

    # Filter out rows from courses that have duplicate cid
    meetings_to_insert = meetings[~meetings["mid"].isin(existing_mids)]

    # Define your SQL table structure with 'mid' as an Integer
    meetings_to_insert.to_sql(
        "meeting",
        engine,
        if_exists="append",
        index=False,
        dtype={
            "mid": Integer(),  # Define mid as Integer
            "ccode": String(),
            "starttime": DateTime(),
            "endtime": DateTime(),
            "cdays": String(),
        },
        method="multi",
    )


def load_requisite(requisites, engine):
    requisites["preReq"] = requisites["preReq"].map({1: True, 0: False})
    requisites.rename(
        columns={"cid": "classid", "requisiteid": "reqid", "preReq": "prereq"},
        inplace=True,
    )
    existing_requisites = pd.read_sql_query(
        "SELECT classid, reqid FROM requisite", engine
    )

    # Remove duplicates from the DataFrame
    new_requisites = requisites.merge(
        existing_requisites, on=["classid", "reqid"], how="left", indicator=True
    )
    new_requisites = new_requisites[new_requisites["_merge"] == "left_only"].drop(
        columns=["_merge"]
    )

    new_requisites.to_sql(
        "requisite", engine, if_exists="append", index=False, dtype={}
    )


def load_room(rooms, engine):
    rooms.rename(columns={"number": "room_number", "id": "rid"}, inplace=True)
    existing_rids = pd.read_sql_query("SELECT rid FROM room", engine)["rid"].tolist()

    # Filter out rows from the DataFrame that have duplicate rid
    new_room = rooms[~rooms["rid"].isin(existing_rids)]

    new_room.to_sql(
        "room",
        engine,
        if_exists="append",
        index=False,
        dtype={
            "building": String(),
            "room_number": String(),
            "capacity": Integer(),
        },
    )


def load_section(sections, engine):
    sections.rename(
        columns={
            "room_id": "roomid",
            "class_id": "cid",
            "meeting_id": "mid",
            "year": "years",
        },
        inplace=True,
    )
    existing_sids = pd.read_sql_query("SELECT sid FROM section", engine)["sid"].tolist()

    # Filter out rows from the DataFrame that have duplicate rid
    new_sections = sections[~sections["sid"].isin(existing_sids)]

    new_sections.to_sql(
        "section",
        engine,
        if_exists="append",
        index=False,
        dtype={
            "roomid": Integer(),
            "cid": Integer(),
            "mid": Integer(),
            "semester": String(),
            "years": String(),
            "capacity": Integer(),
        },
    )


def upload_syllabus(courses):
    """
    It is necessary to download all the course syllabi and store them in the GitHub
    repository {Department-Code-Class-Name.pdf}
    :param courses_df:
    """

    directory_name = os.path.abspath("../syllabuses")
    # Check if the folder exist if not create it
    if not os.path.exists(directory_name):
        os.makedirs(directory_name)
        print(f"Directory '{directory_name} was created.")
    else:
        print(f"Directory '{directory_name} already exists.")

    for _, row in courses.iterrows():
        department = row["cname"]
        code = row["ccode"]
        description = row["description"].replace(" ", "-").replace("/", "-")
        syllabus_url = row["syllabus"]

        file_name = f"{department}-{code}-{description}.pdf"
        file_path = os.path.join(directory_name, file_name)

        # Skip if the syllabus URL is missing or not available
        if pd.isna(syllabus_url) or syllabus_url.lower() == "none":
            print(f"Skipping {file_name}: No syllabus URL available.")
            continue

        try:
            # Download the syllabus PDF
            print(f"Downloading {file_name}...")
            response = requests.get(syllabus_url)
            response.raise_for_status()  # Check if request was successful

            # Save the PDF to the specified path
            with open(file_path, "wb") as f:
                f.write(response.content)

            print(f"Saved: {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Failed to download {file_name}: {e}")


def load_data():
    # Extract data
    courses = get_courses("Data")
    meetings = get_meetings("Data")
    requisites = get_requisites("Data")
    rooms = get_rooms("Data")
    sections = get_sections("Data")

    # Transform data
    sections, meetings, rooms, courses = transform_data(
        sections, meetings, rooms, courses
    )

    # Load data
    engine = create_engine(
        "postgresql+psycopg2://excel:password@localhost:1234/excel_db"
    )
    create_db(engine)
    load_classes(courses, engine)
    load_meeting(meetings, engine)
    load_requisite(requisites, engine)
    load_room(rooms, engine)
    load_section(sections, engine)
    upload_syllabus(courses)
