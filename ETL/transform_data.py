import pandas as pd
import extract_data


def remove_conflicting_sections(sections_df):
    """
    A class cannot have the same section, they must be taught at different hours.
    In case of conflicting hours, the sections with the biggest sid will be removed from
    the set.
    :param sections_df: the dataframe of the sections
    :return: a new dataframe with no section conflict per class
    """

    #This way, rows with the same meeting_id and class_id but higher
    #sid's will be deleted.
    sections_df = sections_df.sort_values(by=['sid'])

    class_meeting_ids = {}

    for index, section in sections_df.iterrows():
        if section['class_id'] not in class_meeting_ids:
            class_meeting_ids[section['class_id']] = []
        # Conflicting section, drop from the frame.
        if section['meeting_id'] in class_meeting_ids[section['class_id']]:
            sections_df.drop(index, inplace=True)
        else:
            class_meeting_ids[section['class_id']].append(section['meeting_id'])

    return sections_df
