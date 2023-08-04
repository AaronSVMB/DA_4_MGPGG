"""
Data cleaning and reading for the power analysis
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================

from constants import pd
from constants import np


# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================


def treatment_reading_and_cleaning(filename:str):
  """
  read and clean the data set so that the subsequent analysis can be conducted efficiently

  :param filename: For the purpose of our power analysis, this is the Shared endowment data
  :return: a pandas dataframe with information on the shared endowment treatment
  """
  # read the data
  treatment_df = pd.read_csv(filename)
  # drop all rows that are demo (not usable data for ANY subsequent analysis)
  treatment_df = treatment_df[~(treatment_df['session.is_demo'] == 1)]
  # drop columns that provide no information and are clutter
  treatment_df.drop(['participant.label','participant._is_bot','participant._index_in_pages',
                     'participant._max_page_index','participant._current_app_name',
                    'participant._current_page_name','participant.time_started_utc',
                    'participant.visited','participant.mturk_worker_id','participant.mturk_assignment_id',
                    'player.role','session.label','session.mturk_HITId','session.mturk_HITGroupId'],
                    axis = 1, inplace = True)
  # make participant id columns integers instead of floats
  columns_to_convert = ['player.blue_group_partner_one_id','player.blue_group_partner_two_id','player.blue_group_partner_three_id',
               'player.green_group_partner_one_id','player.green_group_partner_two_id','player.green_group_partner_three_id']
  treatment_df[columns_to_convert] = treatment_df[columns_to_convert].astype(int)

  treatment_df = treatment_df.reset_index(drop=True)
  return treatment_df


def for_pilot(treatment_df: np.ndarray):
  """
  drop the comprehension question variables; for the real experiment these will be contained in their own app

  :param treatment_df: the cleaned dataframe containing shared endowment datapoints
  :return: the dataframe with the redundant columns removed that were there because of the design of CompQs in the pilot
  """
  treatment_df.drop(['player.comprehension_question_one','player.comprehension_question_two',
                     'player.comprehension_question_three','player.comprehension_question_four_a',
                    'player.comprehension_question_four_b','player.comprehension_question_four_c',
                     'player.comprehension_question_four_d','player.password_to_start'],
                    axis = 1, inplace= True)
  treatment_df = treatment_df.reset_index(drop=True)
  return treatment_df


def shared_endowment(treatment_df: np.ndarray):
  """
  Add binary column that is Shared == True for this data set; useful for when I make a combined data set later on

  :param treatment_df: the shared endowment dataframe
  :return: the shared endowment dataframe with a bool column 1 if shared endwoment 0 else
  """
  treatment_df['session.is_shared'] = True
  return treatment_df


def append_fgf_typing(treatment_df: np.ndarray, smdf: np.ndarray):
  """
  Adds the FGF player typing to the shared/split endowment dataframe : could be useful for subsequent analysis

  :param treatment_df: the treatment dataframe
  :param smdf: the ANALYZED strategy method dataframe
  :return: a combined data frame which adds the player's fgf typing to the treatment dataframe
  """
  merged_df = treatment_df.merge(smdf[['participant.code', 'player.typing']], on='participant.code', how='left')
  return merged_df