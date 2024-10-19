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
    
    # Merge (left join) sections_df and rooms_df where room_id (sections_df) = id (rooms_df)
    merged_df = sections_df.merge(rooms_df, left_on = 'room_id', right_on = 'id', how = 'left')

    # Filter out rows where section capacity is greater than the room capacity
    sections_df = merged_df[merged_df['capacity_x'] <= merged_df['capacity_y']]

    # Eliminate extra columns from join
    sections_df = sections_df.drop(columns=['capacity_y', 'id', 'number', 'building'])

    # Rename column back to capacity
    sections_df = sections_df.rename(columns={'capacity_x': 'capacity'})

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
    
    # Convert class_id and classid to string, and strip leading zeros from classid
    sections_df['class_id'] = sections_df['class_id'].astype(str)
    courses_df['classid'] = courses_df['classid'].astype(str).str.lstrip('0')

    # Merge tables
    merged_df = pd.merge(sections_df, courses_df, left_on='class_id', right_on='classid')

    def is_valid_year(row):
        section_year = row['year']
        course_year_rule = row['years']

        if course_year_rule == 'Odd Years' and section_year % 2 != 0:
            return True
        
        elif course_year_rule == 'Even Years' and section_year % 2 == 0:
            return True
        
        elif course_year_rule == 'Every Year' and section_year != 0:
            return True
        
        elif course_year_rule == 'According to Demand' and section_year != 0:
            return True
        
        return False

    def is_valid_term(row):
        section_semester = row['semester']
        course_term_rule = row['term']

        if course_term_rule == "According to Demand":
            return True

        elif course_term_rule == "First Semester":
            if section_semester == "Fall":
                return True
            else:
                return False

        elif course_term_rule == "Second Semester":
            if section_semester == "Spring":
                return True
            else:
                return False

        elif course_term_rule == "First Semester, Second Semester":
            if section_semester in ["Fall", "Spring"]:
                return True
            else:
                return False

        return False

    merged_df['valid_year'] = merged_df.apply(is_valid_year, axis=1)
    merged_df['valid_term'] = merged_df.apply(is_valid_term, axis=1)

    # Only keep rows that are valid in both year and term
    validated_df = merged_df[(merged_df['valid_year']) & (merged_df['valid_term'])]

    # Keep original sections_df with only valid sections based on 'sid'
    valid_sids = validated_df['sid'].unique()
    sections_df = sections_df[sections_df['sid'].isin(valid_sids)]

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
