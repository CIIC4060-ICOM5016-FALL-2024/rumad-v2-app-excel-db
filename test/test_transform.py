import unittest
import pandas as pd
from ETL.extract_data import *
from ETL.transform_data import remove_conflicting_sections, remove_conflicting_classrooms, cap_sections, \
    correct_section_term

file_path = '../ETL/Data'

class TestRemoveConflictingClassrooms(unittest.TestCase):
    sections = {'sid': [0, 1, 2, 3, 4, 5, 6, 7],
                'room_id':[1, 2, 3, 4, 1, 2, 3, 4],
                'meeting_id':[1, 2, 3, 4, 1, 2, 3, 4],
                'class_id':[1, 2, 3, 4, 1, 2, 3, 4],
                'semester':['Fall', 'Spring', 'V1', 'V2', 'Fall', 'Spring', 'V1', 'V2'],
                'year':[2021, 2022, 2023, 2024, 2021, 2022, 2023, 2024],
                'capacity':[10, 20, 30, 40, 50, 60, 70, 80]}

    expected_sections = {'sid': [0, 1, 2, 3],
                'room_id':[1, 2, 3, 4],
                'meeting_id':[1, 2, 3, 4],
                'class_id':[1, 2, 3, 4],
                'semester':['Fall', 'Spring', 'V1', 'V2'],
                'year':[2021, 2022, 2023, 2024],
                'capacity':[10, 20, 30, 40]}

    sections_df = pd.DataFrame(sections)
    expected_sections_df = pd.DataFrame(expected_sections)

    def test_remove_conflicting_classrooms(self):
        sections_df = remove_conflicting_classrooms(self.sections_df)
        self.assertEqual(self.expected_sections_df.shape, sections_df.shape)

class TestRemoveConflictingSections(unittest.TestCase):
    sections = {'sid': [0, 1, 2, 3, 4, 5, 6, 7],
                'room_id':[1, 2, 3, 4, 5, 6, 7, 8],
                'meeting_id':[1, 2, 3, 4, 1, 2, 3, 4],
                'class_id':[1, 2, 3, 4, 1, 2, 3, 4],
                'semester':['Fall', 'Spring', 'V1', 'V2', 'Fall', 'Spring', 'V1', 'V2'],
                'year':[2021, 2022, 2023, 2024, 2021, 2022, 2023, 2024],
                'capacity':[10, 20, 30, 40, 50, 60, 70, 80]}

    expected_sections = {'sid': [0, 1, 2, 3],
                'room_id':[1, 2, 3, 4],
                'meeting_id':[1, 2, 3, 4],
                'class_id':[1, 2, 3, 4],
                'semester':['Fall', 'Spring', 'V1', 'V2'],
                'year':[2021, 2022, 2023, 2024],
                'capacity':[10, 20, 30, 40]}

    sections_df = pd.DataFrame(sections)
    expected_sections_df = pd.DataFrame(expected_sections)

    def test_remove_conflicting_sections(self):
        sections_df = remove_conflicting_sections(self.sections_df)
        self.assertEqual(self.expected_sections_df.shape, sections_df.shape)


class TestCapSections(unittest.TestCase):

    sections_df = get_sections(file_path)
    rooms_df = get_rooms(file_path)

    def count_overcapacity(self):
        n_over_capacity = 0
        n_invalid = 0
        for index, section in self.sections_df.iterrows():
            try:
                i = self.rooms_df[self.rooms_df['id'] == section['room_id']].index[0]
                room = self.rooms_df.loc[i]
            except (KeyError, IndexError):
                n_invalid += 1
                continue
            if section['capacity'] > room['capacity']:
                n_over_capacity += 1
        return n_over_capacity, n_invalid

    def test_cap_sections(self):
        n_sections_to_remove, n_invalid = self.count_overcapacity()
        n_sections = self.sections_df.shape[0]

        sections_df = cap_sections(self.sections_df, self.rooms_df)

        sections_under_capacity = sections_df.shape[0]

        n_removed_sections = n_sections - sections_under_capacity

        self.assertEqual(n_sections_to_remove + n_invalid, n_removed_sections)

class TestCorrectSectionTerm(unittest.TestCase):
    sections_df = get_sections(file_path)
    courses_df = get_courses(file_path)

    def count_incorrect_terms(self):
        n_incorrect_year = 0
        n_incorrect_term = 0
        n_invalid_course = 0
        for index, section in self.sections_df.iterrows():
            try:
                course_index = self.courses_df[self.courses_df['cid'] == section['class_id']].index[0]
                course = self.courses_df.loc[course_index]
            except (KeyError, IndexError):
                n_invalid_course += 1
                continue
            if course['years'] == 'Even Years':
                if section['year'] % 2 != 0:
                    n_incorrect_year += 1
                    continue
            elif course['years'] == 'Odd Years':
                if section['year'] % 2 == 0:
                    n_incorrect_year += 1
                    continue

            if course['term'] == 'First Semester' and section['semester'] != 'Fall':
                n_incorrect_term += 1
                continue
            elif course['term'] == 'Second Semester' and section['semester'] != 'Spring':
                n_incorrect_term += 1
                continue
            elif course['term'] == 'First Semester, Second Semester' and (section['semester'] != 'Fall' or section['semester'] != 'Spring'):
                n_incorrect_term += 1
                continue

        return n_incorrect_year, n_incorrect_term, n_invalid_course

    def test_correct_section_term(self):
        n_incorrect_year, n_incorrect_term, n_invalid_course = self.count_incorrect_terms()
        n_sections = self.sections_df.shape[0]
        sections_df = correct_section_term(self.sections_df, self.courses_df)
        n_removed_sections = n_sections - sections_df.shape[0]
        print(f'\nThere were {n_incorrect_year} sections with incorrect year')
        print(f'There were {n_incorrect_term} sections with incorrect term')
        print(f'There were {n_invalid_course} sections with invalid course')
        print(f'correct_section_term deleted {n_removed_sections} sections')
        self.assertEqual(n_incorrect_year + n_incorrect_term + n_invalid_course, n_removed_sections)








if __name__ == '__main__':
    unittest.main()
