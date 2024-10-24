import psycopg2
import pandas as pd
from ETL.extract_data import get_sections, get_meetings, get_rooms, get_courses, get_requisites
from ETL.transform_data import transform_data
import os
import requests

def create_db(cursor):
    """
    Creates tables for classes, meetings, requisites, rooms, sections, and syllabi,
    setting up relationships and handling ownership and execution errors.

    :param cursor:
    """
    sql_commands = """
        CREATE TABLE IF NOT EXISTS class (
            cid       SERIAL PRIMARY KEY,
            cname     VARCHAR,
            ccode     VARCHAR,
            cdesc     VARCHAR,
            term      VARCHAR,
            years     VARCHAR,
            cred      INTEGER,
            csyllabus VARCHAR
        );

        CREATE TABLE IF NOT EXISTS meeting (
            mid       SERIAL PRIMARY KEY,
            ccode     VARCHAR,
            starttime TIMESTAMP,
            endtime   TIMESTAMP,
            cdays     VARCHAR
        );

        CREATE TABLE IF NOT EXISTS requisite (
            classid INTEGER NOT NULL REFERENCES class(cid),
            reqid   INTEGER NOT NULL REFERENCES class(cid),
            prereq  BOOLEAN,
            PRIMARY KEY (classid, reqid)
        );

        CREATE TABLE IF NOT EXISTS room (
            rid         SERIAL PRIMARY KEY,
            building    VARCHAR,
            room_number VARCHAR,
            capacity    INTEGER
        );

        CREATE TABLE IF NOT EXISTS section (
            sid      SERIAL PRIMARY KEY,
            roomid   INTEGER REFERENCES room(rid),
            cid      INTEGER REFERENCES class(cid),
            mid      INTEGER REFERENCES meeting(mid),
            semester VARCHAR,
            years    VARCHAR,
            capacity INTEGER
        );

        CREATE TABLE IF NOT EXISTS syllabus (
            chunkid        SERIAL PRIMARY KEY,
            courseid       INTEGER REFERENCES class(cid),
            embedding_text INT2VECTOR,
            chunk          VARCHAR
        );
    """

    cursor.execute(sql_commands)

def load_classes(courses, cursor):
    """
    Loads course data into the 'class' table, ensuring no duplicate entries by filtering existing cids.

    :param courses:
    :param cursor:
    """

    insert_query = """
            INSERT INTO class (cid, cname, ccode, cdesc, term, years, cred, csyllabus) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (cid) DO UPDATE SET 
                cname = EXCLUDED.cname,
                ccode = EXCLUDED.ccode,
                cdesc = EXCLUDED.cdesc,
                term = EXCLUDED.term,
                years = EXCLUDED.years,
                cred = EXCLUDED.cred,
                csyllabus = EXCLUDED.csyllabus;
        """
    for index, row in courses.iterrows():
        cursor.execute(insert_query, (
            row['classid'],
            row['cname'],
            row['ccode'],
            row['description'],
            row['term'],
            row['years'],
            row['cred'],
            row['syllabus']
        ))

def load_meeting(meetings, cursor):
    """
    Loads meeting data into the 'meeting' table, converting date columns,
    renaming fields, and filtering out duplicate mids.

    :param meetings:
    :param cursor:
    """
    insert_query = """
            INSERT INTO meeting (mid, ccode, starttime, endtime, cdays) 
            VALUES (%s, %s, %s, %s, %s) 
            ON CONFLICT (mid) DO UPDATE SET 
                ccode = EXCLUDED.ccode,
                starttime = EXCLUDED.starttime,
                endtime = EXCLUDED.endtime,
                cdays = EXCLUDED.cdays;
        """
    meetings['start'] = pd.to_datetime(meetings['start'])
    meetings['end'] = pd.to_datetime(meetings['end'])
    for index, row in meetings.iterrows():
        cursor.execute(insert_query, (
            row['mid'],
            row['ccode'],
            row['start'],
            row['end'],
            row['day'],
        ))

def load_requisite(requisites, cursor):
    """
    Loads meeting data into the 'meeting' table, converting date columns and avoiding duplicate entries based on existing mids.

    :param requisites:
    :param cursor:
    """

    insert_query = """
                INSERT INTO requisite (classid, reqid, prereq) 
                VALUES (%s, %s, %s)
                ON CONFLICT (classid, reqid) DO UPDATE SET prereq = EXCLUDED.prereq
            """
    requisites['preReq'] = requisites['preReq'].map({1: True, 0: False})
    for index, row in requisites.iterrows():
        cursor.execute(insert_query, (
            row['cid'],
            row['requisiteid'],
            row['preReq'],
        ))

def load_room(rooms, cursor):
    """
    Loads room data into the 'room' table, renaming columns and filtering out duplicate rids.

    :param rooms:
    :param engine:
    """
    insert_query = """
                        INSERT INTO room (rid, building, room_number, capacity) 
                        VALUES (%s, %s, %s, %s)
                        ON CONFLICT (rid) DO UPDATE SET 
                            building = EXCLUDED.building,
                            room_number = EXCLUDED.room_number,
                            capacity = EXCLUDED.capacity;
                    """
    for index, row in rooms.iterrows():
        cursor.execute(insert_query, (
            row['id'],
            row['building'],
            row['number'],
            row['capacity'],
        ))


def load_section(sections, cursor):
    """
    Loads section data into the 'section' table, renaming columns and filtering out duplicate sids.

    :param sections:
    :param cursor:
    """
    insert_query = """
                        INSERT INTO section (sid, roomid, cid, mid, semester, years, capacity) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s)
                        ON CONFLICT (sid) DO UPDATE SET 
                            roomid = EXCLUDED.roomid,
                            cid = EXCLUDED.cid,
                            mid = EXCLUDED.mid,
                            semester = EXCLUDED.semester,
                            years = EXCLUDED.years,
                            capacity = EXCLUDED.capacity;
                    """
    for index, row in sections.iterrows():
        cursor.execute(insert_query, (
            row['sid'],
            row['room_id'],
            row['class_id'],
            row['meeting_id'],
            row['semester'],
            row['year'],
            row['capacity'],
        ))

def upload_syllabus(courses):
    """
    Uploads all the course syllabi and store them in the GitHub
    repository syllabuses
    format: {Department-Code-Class-Name.pdf}

    :param courses:
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
    """
    Extracts, transforms, and loads data into the database by fetching course-related data,
    transforming it, and inserting it into the appropriate tables using a PostgreSQL engine.
    """

    # Extract data
    courses = get_courses('Data')
    meetings = get_meetings('Data')
    requisites = get_requisites('Data')
    rooms = get_rooms('Data')
    sections = get_sections('Data')

    # Transform data
    sections, meetings, rooms, courses = transform_data(sections, meetings, rooms, courses)

    # Load data
    engine = psycopg2.connect(
        dbname="dc79t7ga9hc6ud",
        user="ufm5iffjti843g",
        password="p714ce504f5566ea5085651f4627a98521b24b94298c88546efee8a7e038ad933",
        host="cbdhrtd93854d5.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com",
        port="5432"
    )
    cursor = engine.cursor()
    create_db(cursor)
    load_classes(courses, cursor)
    load_meeting(meetings, cursor)
    load_requisite(requisites, cursor)
    load_room(rooms, cursor)
    load_section(sections, cursor)

    engine.commit()
    if cursor:
        cursor.close()
    if engine:
        engine.close()

