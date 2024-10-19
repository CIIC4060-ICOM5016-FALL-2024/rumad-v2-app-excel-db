import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import json


def get_courses(file_path):
    """

    :param file_path:
    :return:
    """
    tree = ET.parse(file_path + '/courses.xml')
    root = tree.getroot()
    courses_set = []

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

        courses_set.append(record_data)

    return pd.DataFrame(courses_set)


def get_sections(file_path):
    """

    :param file_path:
    :return:
    """
    sections_csv = pd.read_csv(file_path + '/sections.csv')
    return pd.DataFrame(sections_csv)


def get_meetings(file_path):
    """

    :param file_path:
    :return:
    """
    meeting_csv = pd.read_csv(file_path + '/meeting.csv')
    return pd.DataFrame(meeting_csv)


def get_rooms(file_path):
    """

    :param file_path:
    :return:
    """
    with open(file_path + '/rooms.json', 'r') as json_file:
        rooms_json = json.load(json_file)
    rooms_set = []
    for building in rooms_json:
        for room in rooms_json[building]:
            room['building'] = building
            rooms_set.append(room)
    return pd.DataFrame(rooms_set)


def get_requisites(file_path):
    """

    :param file_path:
    :return:
    """
    conn = sqlite3.connect(file_path + '/requisites.db')
    requisites = pd.read_sql_query('SELECT * FROM requisites', conn)
    conn.close()
    return requisites