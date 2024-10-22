import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import json
from datetime import datetime


def get_courses(file_path):
    """

    :param file_path:
    :return:
    """
    tree = ET.parse(file_path + "/courses.xml")
    root = tree.getroot()
    courses_set = []

    for course in root.findall("Courses"):
        record_data = {}

        classes = course.find("classes")
        if classes is not None:
            record_data["ccode"] = classes.find("code").text
            record_data["cname"] = classes.find("name").text

        record_data["classid"] = int(course.find("classid").text)
        record_data["cred"] = int(course.find("cred").text)
        record_data["description"] = course.find("description").text
        record_data["syllabus"] = course.find("syllabus").text
        record_data["term"] = course.find("term").text
        record_data["years"] = course.find("years").text

        courses_set.append(record_data)

    return pd.DataFrame(courses_set)


def get_sections(file_path):
    """

    :param file_path:
    :return:
    """
    sections_csv = pd.read_csv(file_path + "/sections.csv")
    return pd.DataFrame(sections_csv)


def get_meetings(file_path):
    """

    :param file_path:
    :return:
    """
    meeting_csv = pd.read_csv(file_path + "/meeting.csv")

    # Better to do it here
    # Function to convert 'start' and 'end' to datetime.time objects
    def convert_time(meeting):
        meeting["start"] = datetime.strptime(meeting["start"], "%H:%M:%S")
        meeting["end"] = datetime.strptime(meeting["end"], "%H:%M:%S")
        return meeting

    meetings_df = meeting_csv.apply(convert_time, axis=1)
    return meetings_df


def get_rooms(file_path):
    """

    :param file_path:
    :return:
    """
    with open(file_path + "/rooms.json", "r") as json_file:
        rooms_json = json.load(json_file)
    rooms_set = []
    for building in rooms_json:
        for room in rooms_json[building]:
            room["building"] = building
            rooms_set.append(room)
    return pd.DataFrame(rooms_set)


def get_requisites(file_path):
    """

    :param file_path:
    :return:
    """
    conn = sqlite3.connect(file_path + "/requisites.db")
    requisites = pd.read_sql_query("SELECT * FROM requisites", conn)
    conn.close()
    return requisites
