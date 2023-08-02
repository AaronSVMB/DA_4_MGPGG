"""
Data cleaning and reading code for Strategy Method data 
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================


def sm_reading_and_cleaning(filename: str):
  """
  reads a csv file and removes any demo data from the file and drops columns 
  that are irrelevant to our analysis

  :param filename - the csv filename with relevant pathing information
  :return: a np.ndarray with rows and columns containing data from the strategy
  method portion of this experiment
  """
  # Read the data 
  dataframe = pd.read_csv(filename)
  # drop all rows that are demo (not usable data for ANY subsequent analysis)
  dataframe = dataframe[~(dataframe['session.is_demo'] == 1)]
  # drop columns that provide no information and are clutter
  dataframe.drop(['participant.label','participant._is_bot',
           'participant._index_in_pages','participant._max_page_index',
           'participant._current_app_name','participant._current_page_name',
           'participant.time_started_utc','participant.visited',
           'participant.mturk_worker_id','participant.mturk_assignment_id',
           'player.role','session.mturk_HITId','session.mturk_HITGroupId'],
          axis = 1, inplace = True)
  dataframe = dataframe.reset_index(drop=True)
  return dataframe
