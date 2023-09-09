"""
Data cleaning and reading code for Risk Preference data 
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================

def rp_reading_and_cleaning(filename: str):
    """
    Takes in the Risk Preference Data Set (across all sessions) from oTree and cleans the data in the following way

    :param filename: the oTree .csv file for the Risk Preference App
    :return dataframe: the cleaned dataframe corresponding to Risk Preference data from all subjects
    """

    # Read the data
    dataframe = pd.read_csv(filename)
    # drop all rows that are demo (not usable data for ANY subsequent analysis)
    dataframe = dataframe[~(dataframe['session.is_demo'] == 1)]
    # drop unneccessary columns (clutter)
    dataframe.drop(['participant.label', 'participant._is_bot', 'participant._index_in_pages', 
                    'participant._max_page_index', 'participant._current_app_name', 'participant._current_page_name',
                    'participant.time_started_utc', 'participant.visited', 'participant.mturk_worker_id',
                    'participant.mturk_assignment_id', 'player.role', 'session.label', 
                    'session.mturk_HITId', 'session.mturk_HITGroupId', 'session.comment'],
                    axis = 1, inplace=True)
    # reset indices
    dataframe = dataframe.reset_index(drop=True)
    return dataframe
