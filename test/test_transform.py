import unittest
import pandas as pd
from ETL.extract_data import *
from ETL.transform_data import remove_conflicting_sections, remove_conflicting_classrooms, cap_sections

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
        self.assertEqual(sections_df.shape, self.expected_sections_df.shape)

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
        self.assertEqual(sections_df.shape, self.expected_sections_df.shape)


class TestCapSections(unittest.TestCase):

    sections_df = get_sections(file_path)
    rooms_df = get_rooms(file_path)

    def count_overcapacity(self):
        count = 0
        for index, section in self.sections_df.iterrows():
            try:
                i = self.rooms_df[self.rooms_df['id'] == section['room_id']].index[0]
                room = self.rooms_df.loc[i]
            except (KeyError, IndexError):
                continue
            if section['capacity'] > room['capacity']:
                count += 1
        return count

    def test_cap_sections(self):
        n_sections_to_remove = self.count_overcapacity()
        n_sections = self.sections_df.shape[0]

        sections_df = cap_sections(self.sections_df, self.rooms_df)

        sections_under_capacity = sections_df.shape[0]

        n_removed_sections = n_sections - sections_under_capacity

        self.assertEqual(n_removed_sections, n_sections_to_remove)



if __name__ == '__main__':
    unittest.main()
