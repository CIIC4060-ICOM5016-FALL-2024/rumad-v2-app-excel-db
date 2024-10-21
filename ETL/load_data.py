from sqlalchemy import create_engine, Integer, String, DateTime, text
import pandas as pd
from ETL.extract_data import get_sections, get_meetings, get_rooms, get_courses, get_requisites
from ETL.transform_data import transform_data

def load_classes(courses, engine):
    courses['cred'] = pd.to_numeric(courses['cred'], errors='coerce')
    courses['cred'] = courses['cred'].fillna(0)
    courses.rename(columns={'classid': 'cid','name': 'cname', 'code': 'ccode', 'description': 'cdesc', 'syllabus': 'csyllabus'}, inplace=True)
    courses.to_sql('class', engine, if_exists='replace', index=False, dtype={
        'cid': Integer(),
        'cname': String(),
        'ccode': String(),
        'cdesc': String(),
        'term': String(),
        'years': String(),
        'cred': Integer(),
        'csyllabus': String()
    })

def load_meeting(meetings, engine):
    meetings['start'] = pd.to_datetime(meetings['start'])
    meetings['end'] = pd.to_datetime(meetings['end'])
    meetings.rename(columns={'start': 'starttime', 'end': 'endtime', 'day': 'cdays'}, inplace=True)

    # Define your SQL table structure with 'mid' as an Integer
    meetings.to_sql('meeting', engine, if_exists='replace', index=False, dtype={
        'mid': Integer(),  # Define mid as Integer
        'ccode': String(),
        'starttime': DateTime(),
        'endtime': DateTime(),
        'cdays': String()
    }, method='multi')

def load_requisite(requisites, engine):
    requisites.to_sql('requisite', engine, if_exists='replace', index=False, dtype={})

def load_room(rooms, engine):
    rooms.rename(columns={'number': 'room_number'}, inplace=True)
    rooms.to_sql('room', engine, if_exists='replace', index=False, dtype={
        'building': String(),
        'room_number': String(),
        'capacity': Integer(),
    })

def load_section(sections, engine):
    sections.rename(columns={'room_id': 'roomid', 'class_id': 'cid', 'meeting_id': 'mid', 'year':'years'}, inplace=True)
    sections.to_sql('section', engine, if_exists='replace', index=False, dtype={
        'roomid': Integer(),
        'cid': Integer(),
        'mid': Integer(),
        'semester': String(),
        'years': String(),
        'capacity': Integer(),
    })

def load_data():
    # Extract data
    courses = get_courses('Data')
    meetings = get_meetings('Data')
    requisites = get_requisites('Data')
    rooms = get_rooms('Data')
    sections = get_sections('Data')

    c = len(courses.values.tolist())
    m = len(meetings.values.tolist())
    # re = requisites
    ro = len(rooms.values.tolist())
    s = len(sections.values.tolist())
    # Transform data
    transform_data(sections, meetings, rooms, courses)
    print("Courses cleanse before", c,"after",len(courses.values.tolist()))
    print("Meetings cleanse before", m, "after",len(meetings.values.tolist()))
    print("Room cleanse before", ro, "after",len(rooms.values.tolist()))
    print("Sections cleanse before", s, "after",len(sections.values.tolist()))
    # Load data
    engine = create_engine('postgresql+psycopg2://excel:password@localhost:1234/excel_db')
    load_classes(courses, engine)
    load_meeting(meetings, engine) # DONE
    load_requisite(requisites, engine) # DONE
    load_room(rooms, engine) # DONE
    load_section(sections, engine) # DONE

load_data()