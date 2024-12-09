import pandas as pd

def get_clean_classes(file_path):
    classes = pd.read_csv(file_path + "/class.csv")
    return classes

def get_clean_meetings(file_path):
    meetings = pd.read_csv(file_path + "/meeting.csv")
    return meetings

def get_clean_requisites(file_path):
    requisites = pd.read_csv(file_path + "/requisite.csv")
    return requisites

def get_clean_rooms(file_path):
    rooms = pd.read_csv(file_path + "/room.csv")
    return rooms

def get_clean_sections(file_path):
    sections = pd.read_csv(file_path + "/section.csv")
    return sections
