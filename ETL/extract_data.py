import xml.etree.ElementTree as ET
import pandas as pd
import sqlite3
import json
from datetime import datetime
import os
import requests


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


def get_syllabus(courses_df):
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

    for _, row in courses_df.iterrows():
        department = row["name"]
        code = row["code"]
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
