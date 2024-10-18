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
        self.assertEqual(2, self.courses_df['cid'].iloc[0])


class TestSections(unittest.TestCase):
    sections_df = get_sections(file_path)

    def test_empty(self):
        self.assertGreater(len(self.sections_df), 0)


class TestMeetings(unittest.TestCase):
    meetings_df = get_meetings(file_path)

    def test_empty(self):
        self.assertGreater(len(self.meetings_df), 0)


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
