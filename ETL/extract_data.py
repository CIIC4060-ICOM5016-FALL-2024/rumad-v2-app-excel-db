import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import json

def extract_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    data = []
    
    for course in root.findall('Courses'):
        record_data = {}
        
        classes = course.find('classes')
        if classes is not None:
            record_data['code'] = classes.find('code').text
            record_data['name'] = classes.find('name').text

        record_data['classid'] = course.find('classid').text
        record_data['cred'] = course.find('cred').text
        record_data['description'] = course.find('description').text
        record_data['syllabus'] = course.find('syllabus').text
        record_data['term'] = course.find('term').text
        record_data['years'] = course.find('years').text
        
        data.append(record_data)

    return pd.DataFrame(data)

courses_df = extract_xml('ETL/courses.xml')

try:
    courses_df = extract_xml('ETL/courses.xml')
    
    meeting_df = pd.read_csv('ETL/meeting.csv')
    print(meeting_df)
    sections_df = pd.read_csv('ETL/sections.csv')
    
    with open('ETL/rooms.json', 'r') as f:
        rooms_data = json.load(f)

    data = [(building, room['number'], room['capacity']) for building, rooms in rooms_data.items() for room in rooms]

    rooms_df = pd.DataFrame(data, columns=['building', 'room_number', 'capacity'])
    print(rooms_df)
        
    conn = sqlite3.connect('ETL/requisites.db')
    requisites_df = pd.read_sql_query("SELECT * FROM requisites", conn)
    conn.close()

except FileNotFoundError as e:
    print(f"File not found: {e.filename}")
except sqlite3.Error as e:
    print(f"Database error: {e}")
except json.JSONDecodeError:
    print("Error decoding JSON file.")
except Exception as e:
    print(f"An error occurred: {e}")
