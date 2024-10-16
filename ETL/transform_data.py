import pandas as pd
import extract_data


def offset_ids(courses_df):
    """
    The classes data starts with id 2.
    :param courses_df: the daframe of the courses
    :return: a new dataframe where cid >= 2
    """
    # Anthony codes here
    return courses_df


def remove_conflicting_classrooms(sections_df):
    """
    Two sections cannot be taught at the same hour in the same classroom.
    Drops sections with conflicting classrooms after one has been set first.

    :param sections_df: the dataframe of the courses
    :return: a new dataframe where a section does not have conflicting classrooms in the
    same academic term (Fall, Spring, V1, V2)
    """
    # Anthony codes here
    return sections_df


def remove_conflicting_sections(sections_df):
    """
    A class cannot have the same section, they must be taught at different hours.
    In case of conflicting hours, the sections with the biggest sid will be removed from
    the set.
    :param sections_df: the dataframe of the sections
    :return: a new dataframe with no section conflict per class
    """

    # This way, rows with the same meeting_id and class_id but higher
    # sid's will be deleted.
    sections_df = sections_df.sort_values(by=['sid'])

    class_meeting_ids = {}

    # Doesn't handle academic term. Need to modify.
    for index, section in sections_df.iterrows():
        if section['class_id'] not in class_meeting_ids:
            class_meeting_ids[section['class_id']] = []
        # Conflicting section, drop from the frame.
        if section['meeting_id'] in class_meeting_ids[section['class_id']]:
            sections_df.drop(index, inplace=True)
        else:
            class_meeting_ids[section['class_id']].append(section['meeting_id'])

    return sections_df


def apply_universal_time(sections_df, meetings_df):
    """
    Meetings ‘MJ’ are from 7:30 a.m.-10:15 a.m. and 12:30 p.m.-7:45 p.m. Any section in between
    shall be removed. Any section after the hour must be removed. If any section overlaps, you will
    add the necessary time to not overlap.
    :param sections_df: the dataframe of the sections
    :param meetings_df: the dataframe of the meetings
    :return: a new dataframe where sections respect the universal time
    """
    # Edimar codes here
    return sections_df


def cap_sections(sections_df, rooms_df):
    """
    Sections cannot be in overcapacity, classrooms have limits.
    :param sections_df: the dataframe of the sections
    :param rooms_df: the dataframe of the rooms
    :return: a new dataframe where the section capacity does not exceed the
    classroom capacity
    """
    # Glerys codes here
    return sections_df


def correct_section_term(sections_df, courses_df):
    """
    Courses must be taught in the correct year and correct semester.
    a. First semester = Fall
    b. Second semester = Spring
    c. According to demand = Any moment of the year (Summer included)

    :param sections_df: the dataframe of the sections
    :param courses_df: the dataframe of the courses
    :return: a new dataframe where the section term is correct according
    course dataframe
    """
    # Glerys codes here
    return sections_df


def delete_invalid_sections(courses_df, sections_df, meetings_df, rooms_df):
    """
    Sections must be taught in a valid classroom and meeting, and the class must exist. If any of
    these values are missing or invalid, you must delete said record.
    :param courses_df: the dataframe of the courses
    :param sections_df: the dataframe of the sections
    :param meetings_df: the dataframe of the meetings
    :param rooms_df: the dataframe of the rooms
    :return: a new dataframe where the sections are valid
    """
    # Anthony codes here
    return sections_df

