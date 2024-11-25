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
            cid       SERIAL PRIMARY KEY, CHECK(cid >= 2),
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
            cdays     VARCHAR CHECK(cdays IN ('MJ', 'LWV'))
        );
        
        CREATE OR REPLACE FUNCTION check_meeting_duration()
        RETURNS TRIGGER AS $$
        DECLARE 
            duration INTERVAL;
        BEGIN
        
        duration := NEW.endtime - NEW.starttime;
        
        IF NEW.cdays = 'MJ' THEN
            IF duration <> INTERVAL '01:15:00' THEN
                RAISE EXCEPTION 'Invalid duration (%) for a MJ meeting: (75 minutes)',
                duration;
            END IF;
        ELSIF NEW.cdays = 'LWV' THEN
            IF duration <> INTERVAL '00:50:00' THEN
                RAISE EXCEPTION 'Invalid duration (%) for a LMV meeting: (50 minutes)',
                duration;
            END IF;  
        END IF;
        
        RETURN NEW;
        
        END;
        
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER check_meeting_time
        BEFORE INSERT OR UPDATE ON meeting
        FOR EACH ROW
        EXECUTE FUNCTION check_meeting_duration();

        CREATE TABLE IF NOT EXISTS requisite (
            classid INTEGER NOT NULL REFERENCES class(cid) ON DELETE CASCADE,
            reqid   INTEGER NOT NULL REFERENCES class(cid) ON DELETE CASCADE,
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
            roomid   INTEGER REFERENCES room(rid) ON DELETE CASCADE,
            cid      INTEGER REFERENCES class(cid) ON DELETE CASCADE,
            mid      INTEGER REFERENCES meeting(mid) ON DELETE CASCADE,
            semester VARCHAR,
            years    VARCHAR,
            capacity INTEGER,
            UNIQUE (roomid, mid, semester, years),
            UNIQUE (cid, mid, semester, years)
        );
        
        CREATE OR REPLACE FUNCTION check_section_capacity()
        RETURNS TRIGGER AS $$
        DECLARE
            room_capacity INTEGER;
        BEGIN
        
        SELECT capacity INTO room_capacity FROM room WHERE rid = NEW.roomid;
        
        IF NEW.capacity > room_capacity THEN
            RAISE EXCEPTION 'Section capacity (%) exceeds room_capacity (%)', 
            NEW.capacity, room_capacity;
        END IF;
        
        RETURN NEW;
        
        END;
        
        $$ LANGUAGE plpgsql;
        
        CREATE OR REPLACE FUNCTION check_section_class()
        RETURNS TRIGGER AS $$
        DECLARE
            class_term      VARCHAR;
            class_year      VARCHAR;
            section_year    INTEGER;
        BEGIN
        
        SELECT term, years INTO class_term, class_year  FROM class WHERE cid = NEW.cid;
    
        IF class_term = 'First Semester, Second Semester' 
        AND (NEW.semester != 'Fall' AND NEW.semester != 'Spring') THEN
            RAISE EXCEPTION 'Section was set to term (%) but class is offered on (%)',
            NEW.semester, class_term;
        ELSIF class_term = 'First Semester' AND NEW.semester != 'Fall' THEN
            RAISE EXCEPTION 'Section was set to term (%) but class is offered on (%)',
            NEW.semester, class_term;
        ELSIF class_term = 'Second Semester' AND NEW.semester != 'Spring' THEN
            RAISE EXCEPTION 'Section was set to term (%) but class is offered on (%)',
            NEW.semester, class_term;
        END IF;
        
        section_year := CAST(NEW.years AS INTEGER);
        
        IF class_year = 'Even Years' AND (section_year % 2 != 0) THEN
            RAISE EXCEPTION 'Section was set to year (%) but class is offered on (%)',
            NEW.years, class_year;
        END IF;
        
        IF class_year = 'Odd Years' AND (section_year % 2 = 0) THEN
            RAISE EXCEPTION 'Section was set to year (%) but class is offered on (%)',
            NEW.years, class_year;
        END IF;
        
        RETURN NEW;
        
        END;
        
        $$ LANGUAGE plpgsql;
        
        CREATE OR REPLACE FUNCTION section_time_check()
        RETURNS TRIGGER AS $$
        DECLARE
            section_start   TIMESTAMP;
            section_end     TIMESTAMP;
            section_days    VARCHAR;
        BEGIN
        SELECT starttime, endtime, cdays INTO section_start, section_end, section_days FROM meeting WHERE mid = NEW.mid;
        IF section_days = 'MJ' THEN
            IF section_start::time < '07:30:00'::time OR section_start::time > '19:45:00'::time THEN
                RAISE EXCEPTION 'MJ section starts % outside of valid time (7:30AM - 7:45PM)',
                section_start;
            ELSIF section_end::time < '07:30:00'::time OR section_end::time > '19:45:00'::time THEN
                RAISE EXCEPTION 'MJ section ends % outside of valid time (7:30AM - 7:45PM)',
                section_end;
            ELSIF section_end::time > '10:15:00'::time AND (section_end::time < '12:30:00'::time
             OR section_start::time < '12:30:00'::time) THEN 
                RAISE EXCEPTION 'MJ section (% - %) violates universal hour (10:15AM - 12:30PM)',
                section_start, section_end;
            END IF;
        END IF;
        RETURN NEW;
        END;
        $$ LANGUAGE plpgsql;
        
        CREATE TRIGGER section_capacity_check
        BEFORE INSERT OR UPDATE ON section
        FOR EACH ROW
        EXECUTE FUNCTION check_section_capacity();
        
        CREATE TRIGGER section_class_check
        BEFORE INSERT OR UPDATE ON section
        FOR EACH ROW
        EXECUTE FUNCTION check_section_class();
        
        CREATE TRIGGER section_time_check
        BEFORE INSERT OR UPDATE ON section
        FOR EACH ROW
        EXECUTE FUNCTION section_time_check();
        
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

def reset_sequences(cursor):
    """
    Resets serial sequences for all tables to align with the current maximum values.
    :param cursor: Database cursor
    """
    sequence_reset_queries = [
        "SELECT setval(pg_get_serial_sequence('class', 'cid'), COALESCE(MAX(cid), 1)) FROM class;",
        "SELECT setval(pg_get_serial_sequence('meeting', 'mid'), COALESCE(MAX(mid), 1)) FROM meeting;",
        "SELECT setval(pg_get_serial_sequence('room', 'rid'), COALESCE(MAX(rid), 1)) FROM room;",
        "SELECT setval(pg_get_serial_sequence('section', 'sid'), COALESCE(MAX(sid), 1)) FROM section;",
        "SELECT setval(pg_get_serial_sequence('syllabus', 'chunkid'), COALESCE(MAX(chunkid), 1)) FROM syllabus;"
    ]
    for query in sequence_reset_queries:
        cursor.execute(query)


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
    # Test Load data
    # engine = psycopg2.connect(
    #     dbname="excel_db",
    #     user="excel",
    #     password="password",
    #     host="localhost",
    #     port="1234"
    # )

    # Heroku Load data
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
    reset_sequences(cursor)

    engine.commit()
    if cursor:
        cursor.close()
    if engine:
        engine.close()