from datetime import datetime
import pandas as pd


def remove_invalid_ids(courses):
        # remove empty cells
        courses.dropna()
        # remove classes that have an id less than 2
        for x in courses.index:
            if int(courses.loc[x, 'code']) < 2:
                #If course is a placeholder, do not delete
                if courses.loc[x, 'name'] == "Authorization from the Director of the Department":
                    continue
                else:
                    courses.drop(x, inplace=True)

        return courses

def remove_conflicting_classrooms(sections_df):
    """
    Two sections cannot be taught at the same hour in the same classroom.
    Drops sections with conflicting classrooms after one has been set first.

    :param sections_df: the dataframe of the courses
    :return: a new dataframe where a section does not have conflicting classrooms in the
    same academic term (Fall, Spring, V1, V2)
    """
    # Anthony codes here
    sections_df = sections_df.sort_values(by=['sid'])
    classrooms_checker = []

    for index, section in sections_df.iterrows():
        #Take into account academic term
        curr_section = (section['semester'], section['year'], section['meeting_id'], section['room_id'])
        # Conflicting section, drop from the frame.
        if curr_section in classrooms_checker:
            sections_df.drop(index, inplace=True)
        else:
            classrooms_checker.append(curr_section)

    return sections_df


def remove_conflicting_sections(sections_df):
    """
    A class cannot have the same section, they must be taught at different hours.
    In case of conflicting hours, the sections with the biggest sid will be removed from
    the set.
    :param sections_df: the dataframe of the sections
    :return: a new dataframe with no section conflict per class
    """
    sections_df = sections_df.sort_values(by=['sid'])

    class_meeting_ids = {}

    for index, section in sections_df.iterrows():
        if section['class_id'] not in class_meeting_ids:
            class_meeting_ids[section['class_id']] = []

        #Take into account academic term and year
        meeting = (section['semester'], section['year'], section['meeting_id'])

        # Conflicting section, drop from the frame.
        if meeting in class_meeting_ids[section['class_id']]:
            sections_df.drop(index, inplace=True)
        else:
            class_meeting_ids[section['class_id']].append(meeting)

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
    universal_time_start = datetime.strptime("10:15:00", "%H:%M:%S")
    universal_time_end = datetime.strptime("12:30:00", "%H:%M:%S")
    day_end = datetime.strptime("19:45:00", "%H:%M:%S")
    section_time = datetime.strptime("1:15:00", "%H:%M:%S")

    # We'll use a dictionary to accommodate sections for each classroom.
    # Common sense? Maybe. Obviously run this function after resolving conflicts, or
    # it will blow up in our faces.
    classroom_schedule = {}

    for index, section in sections_df.iterrows():

        # Try to locate meeting. This ignores nonexistent ones
        try:
            meeting = meetings_df.loc[section['meeting_id'] - 1]  # to offset for the dataframe index
        except KeyError:
            continue

        # Do our checks now to not add trash to the dictionary
        if meeting['day'] == 'LWV':
            # We ignore LWV
            continue

        if meeting['start'] > day_end or meeting['end'] > day_end:
            # Can't add time for these sections.
            sections_df.drop(index, inplace=True)
            continue

        if meeting['start'] >= universal_time_start and meeting['end'] < universal_time_end:
            # Completely inside the universal time. Can't save it.
            sections_df.drop(index, inplace=True)
            continue

        # Create that classroom key as a tuple.
        classroom = (section['room_id'], section['semester'], section['year'])

        # Add that specific time classroom
        if classroom not in classroom_schedule:
            classroom_schedule[classroom] = []

        # All we have left is valid MJ times and times that need shifting
        # We need to attach the section id to the meeting so
        # it can be traced back and updated.

        meeting = meeting.copy()  # To avoid Pandas warnings.

        meeting['sid'] = section['sid']
        classroom_schedule[classroom].append(meeting)  # it works by the grace of God

    # For simplicity, lets create many new temporary dataframes for
    # observing the timeline of a classroom in the academic semester

    for classroom in classroom_schedule:
        print(classroom)
        classroom_df = pd.DataFrame(classroom_schedule[classroom])
        classroom_df = classroom_df.sort_values(by=['mid'])
        print(classroom_df)

        # a backup if a sections goes out of bounds
        #sections_copy_df = sections_df.copy()

        # We need to find overlapping and subsequent sections and shift their
        # mid by +1
        # HOWEVER, how do I 'add' time if I can't change the keys or modify the meetings?

    return sections_df

# I think we can put this in the test suite.
def correct_meeting_duration(meetings_df):
    """
    Check if LWV classes are of 50 minutes, if false remove it from the dataframe.
    Check if MJ classes are of 75 minutes, if false remove it from the dataframe.
    :param meetings_df: the dataframe of the meetings
    """
    for index, meeting in meetings_df.iterrows():
        time_start = meeting['start']
        time_end = meeting['end']
        if meeting['day'] == "MJ" and str(time_end - time_start) != "1:15:00":
            print("MJ Wrong Time: ", meeting['start'], meeting['end'])
            meetings_df.drop(index, inplace=True)
        if meeting['day'] == "LWV" and str(time_end - time_start) != "0:50:00":
            print("LWV Wrong Time: ", meeting['start'], meeting['end'])
            meetings_df.drop(index, inplace=True)

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
    # transform classid from a str list to an int list
    class_id_list = [int(i) for i in courses_df['classid'].values.tolist()]

    for x in sections_df.index:
        # Check if room, class and meeting exist. If not, delete the record.
        if (sections_df.loc[x, 'room_id'] not in rooms_df['id'].values.tolist()
            or sections_df.loc[x, 'class_id'] not in class_id_list
                or sections_df.loc[x, 'meeting_id'] not
                in meetings_df['mid'].values.tolist()):
            sections_df.drop(x, inplace=True)

    return sections_df
