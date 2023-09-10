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

  :param filename: the csv filename with relevant pathing information
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
           'player.role', 'session.label', 'session.mturk_HITId',
           'session.mturk_HITGroupId', 'session.comment'],
          axis = 1, inplace = True)
  dataframe = dataframe.reset_index(drop=True)
  return dataframe


# ====================================================================================================================
# Merge Strategy Method DF with Strategy Method Instrucs & Comp Qs relevent columns 
# ====================================================================================================================


def sm_merge_game_and_instrucs(smdf: pd.DataFrame, instrucsdf: pd.DataFrame):
  """
  append the instrucsdf relevent data to the smdf for subsequent analysis

  :param smdf: strategy method app dataframe
  :param instrucsdf: instrucs and comp qs app data frame
  :return sm_and_instrucs_df: merged df with relevent content from both
  """
  sm_and_instrucs_df = pd.merge(smdf, instrucsdf[['participant.code','player.comprehension_question_one_part_one',
                                                         'player.comprehension_question_one_part_two', 'player.comprehension_question_two_part_one',
                                                         'player.comprehension_question_two_part_two', 'player.comprehension_question_three_part_one',
                                                         'player.comprehension_question_three_part_two', 'player.comprehension_question_three_part_three',
                                                         'player.comprehension_question_four_part_one', 'player.comprehension_question_four_part_two',
                                                         'player.comprehension_question_four_part_three','player.time_to_answer',
                                                         'player.start_time', 'player.time_spent_instrucs',
                                                         'player.time_spent_q_one', 'player.time_spent_q_two',
                                                         'player.time_spent_q_three', 'player.time_spent_q_four',
                                                         'player.num_errors_q_one_a', 'player.num_errors_q_one_b',
                                                         'player.num_errors_q_two_a', 'player.num_errors_q_two_b',
                                                         'player.num_errors_q_three_a', 'player.num_errors_q_three_b',
                                                         'player.num_errors_q_three_c', 'player.num_errors_q_four_a',
                                                         'player.num_errors_q_four_b', 'player.num_errors_q_four_c',
                                                         ]],
                                                         on='participant.code')
  return sm_and_instrucs_df

