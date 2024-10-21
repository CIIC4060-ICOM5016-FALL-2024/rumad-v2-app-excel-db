import unittest

from ETL.extract_data import *

file_path = '../ETL/Data'


class TestCourses(unittest.TestCase):
    courses_df = get_courses(file_path)

    def test_empty(self):
        self.assertGreater(len(self.courses_df), 0)

    def test_id(self):
        """
        The classes data starts with id 2.
        """
        self.assertEqual(2, self.courses_df['classid'].iloc[0])


class TestSections(unittest.TestCase):
    sections_df = get_sections(file_path)

    def test_empty(self):
        self.assertGreater(len(self.sections_df), 0)


class TestMeetings(unittest.TestCase):
    meetings_df = get_meetings(file_path)

    def test_empty(self):
        self.assertGreater(len(self.meetings_df), 0)

    def test_meeting_duration(self):
        meetings_df = self.meetings_df
        """
        Check if LWV classes are of 50 minutes.
        Check if MJ classes are of 75 minutes.
        :param meetings_df: The dataframe of the meetings
        """
        for index, meeting in meetings_df.iterrows():
            time_start = meeting['start']
            time_end = meeting['end']
            if meeting['day'] == "MJ":
                self.assertEqual("0 days 01:15:00", str(time_end - time_start))
            if meeting['day'] == "LWV":
                self.assertEqual("0 days 00:50:00", str(time_end - time_start))


class TestRooms(unittest.TestCase):
    rooms_df = get_rooms(file_path)

    def test_empty(self):
        self.assertGreater(len(self.rooms_df), 0)


class TestRequisites(unittest.TestCase):
    requisites_df = get_requisites(file_path)

    def test_empty(self):
        self.assertGreater(len(self.requisites_df), 0)


if __name__ == '__main__':
    unittest.main()
