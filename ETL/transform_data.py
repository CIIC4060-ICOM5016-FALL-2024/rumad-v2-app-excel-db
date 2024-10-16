import pandas as pd
import extract_data


# 2. A class cannot have the same section, they must be taught at different hours.
# In case of conflictiong sessions,
def remove_conflicting_sections(sections_df):
    """
    A class cannot have the same section, they must be taught at different hours.
    In case of conflicting hours, the section with the biggest sid will be removed from
    the set.
    :param sections_df: the dataframe of the sections
    :return: a new dataframe with no section conflict per class
    """
    print(sections_df)


remove_conflicting_sections(extract_data.get_sections('Data'))
