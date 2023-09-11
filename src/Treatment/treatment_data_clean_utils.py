"""
Data cleaning and reading code for treatment data (single, split, shared)
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================


def treatment_reading_and_cleaning(filename: str):
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
# Merge Shared DF with treatment Instrucs & Comp Qs relevent columns 
# ====================================================================================================================


def shared_merge_game_and_instrucs(treatment_df: pd.DataFrame, instrucs_df: pd.DataFrame):
    """
    Append the instrucs dataframe to the relevent treatment dataframe

    :param treatment_df: treatment app dataframe
    :param instrucs_df: treatment instructions dataframe
    :return treatment_and_instrucs_df: merged df with relevent columns renamed
    """
    #rename potentially problematic column names before merge
    instrucs_df.rename(columns={
       'player.comprehension_question_one':'player.comprehension_question_one_shared',
       'player.comprehension_question_two':'player.comprehension_question_two_shared',
       'player.comprehension_question_three_a':'player.comprehension_question_three_a_shared',
       'player.comprehension_question_three_b':'player.comprehension_question_three_b_shared',
       'player.comprehension_question_four_a': 'player.comprehension_question_four_a_shared',
       'player.comprehension_question_four_b': 'player.comprehension_question_four_b_shared',
       'player.comprehension_question_four_c': 'player.comprehension_question_four_c_shared',
       'player.comprehension_question_four_d': 'player.comprehension_question_four_d_shared',
       'player.time_to_answer': 'player.time_to_answer_treatment_instrucs',
       'player.start_time': 'player.start_time_treatment_instrucs',
       'player.time_spent_instrucs': 'player.time_spent_instrucs_treatment',
       'player.time_spent_q_one': 'player.time_spent_q_one_treatment',
       'player.time_spent_q_two': 'player.time_spent_q_two_treatment',
       'player.time_spent_q_three': 'player.time_spent_q_three_treatment',
       'player.time_spent_q_four': 'player.time_spent_q_four_treatment',
       'player.num_errors_q_one': 'player.num_errors_q_one_shared',
       'player.num_errors_q_two': 'player.num_errors_q_two_shared',
       'player.num_errors_q_three_a': 'player.num_errors_q_three_a_shared',
       'player.num_errors_q_three_b': 'player.num_errors_q_three_b_shared',
       'player.num_errors_q_four_a': 'player.num_errors_q_four_a_shared',
       'player.num_errors_q_four_b': 'player.num_errors_q_four_b_shared',
       'player.num_errors_q_four_c': 'player.num_errors_q_four_c_shared',
       'player.num_errors_q_four_d': 'player.num_errors_q_four_d_shared'  
               }, inplace=True)

    shared_and_instrucs_df = pd.merge(treatment_df, instrucs_df[['participant.code','player.comprehension_question_one_shared',
                                                                    'player.comprehension_question_two_shared','player.comprehension_question_three_a_shared',
                                                                    'player.comprehension_question_three_b_shared','player.comprehension_question_four_a_shared',
                                                                    'player.comprehension_question_four_b_shared','player.comprehension_question_four_c_shared',
                                                                    'player.comprehension_question_four_d_shared', 'player.time_to_answer_treatment_instrucs',
                                                                    'player.start_time_treatment_instrucs', 'player.time_spent_instrucs_treatment', 
                                                                    'player.time_spent_q_one_treatment', 'player.time_spent_q_two_treatment',
                                                                    'player.time_spent_q_three_treatment', 'player.time_spent_q_four_treatment',
                                                                    'player.num_errors_q_one_shared','player.num_errors_q_two_shared',
                                                                    'player.num_errors_q_three_a_shared','player.num_errors_q_three_b_shared',
                                                                    'player.num_errors_q_four_a_shared','player.num_errors_q_four_b_shared',
                                                                    'player.num_errors_q_four_c_shared','player.num_errors_q_four_d_shared']],
                                         on='participant.code')
    
    shared_and_instrucs_df['Shared'] = True
    shared_and_instrucs_df['Split'] = False
    shared_and_instrucs_df['Single'] = False

    shared_and_instrucs_df.rename(columns={
       'player.payoff':'player.payoff_treatment',
       'player.start_time':'player.start_time_treatment',
       'player.time_spent_results':'player.time_spent_results_treatment',
       'player.time_spent_cumulative_results':'player.time_spent_cumulative_results_treatment',
       'group.id_in_subsession': 'group.id_in_subsession_treatment',
       'subsession.round_number': 'subsession.round_number_treatment'
    })
    return shared_and_instrucs_df


# ====================================================================================================================
# Merge Split DF with treatment Instrucs & Comp Qs relevent columns 
# ====================================================================================================================


def split_merge_game_and_instrucs(treatment_df: pd.DataFrame, instrucs_df: pd.DataFrame):
   """
   Combine the split app and the split instrucs datasets

   :param treatment_df: treatment app dataframe
   :param instrucs_df: treatment instructions dataframe
   :return treatment_and_instrucs_df: merged df with relevent columns renamed
   """
   #rename potentially problematic column names before merge
   instrucs_df.rename(columns={
      'player.comprehension_question_one_blue':'player.comprehension_question_one_blue_split',
      'player.comprehension_question_one_green':'player.comprehension_question_one_green_split',
      'player.comprehension_question_two':'player.comprehension_question_two_split',
      'player.comprehension_question_three_a':'player.comprehension_question_three_a_split',
      'player.comprehension_question_three_b':'player.comprehension_question_three_b_split',
      'player.comprehension_question_four_a':'player.comprehension_question_four_a_split',
      'player.comprehension_question_four_b':'player.comprehension_question_four_b_split',
      'player.comprehension_question_four_c':'player.comprehension_question_four_c_split',
      'player.comprehension_question_four_d':'player.comprehension_question_four_d_split',
      'player.time_to_answer': 'player.time_to_answer_treatment_instrucs',
      'player.start_time':'player.start_time_treatment_instrucs',
      'player.time_spent_instrucs':'player.time_spent_instrucs_treatment',
      'player.time_spent_q_one':'player.time_spent_q_one_treatment',
      'player.time_spent_q_two':'player.time_spent_q_two_treatment',
      'player.time_spent_q_three':'player.time_spent_q_three_treatment',
      'player.time_spent_q_four':'player.time_spent_q_four_treatment',
      'player.num_errors_q_one_blue':'player.num_errors_q_one_blue_split',
      'player.num_errors_q_one_green':'player.num_errors_q_one_green_split',
      'player.num_errors_q_two':'player.num_errors_q_two_split',
      'player.num_errors_q_three_a':'player.num_errors_q_three_a_split',
      'player.num_errors_q_three_b':'player.num_errors_q_three_b_split',
      'player.num_errors_q_four_a':'player.num_errors_q_four_a_split',
      'player.num_errors_q_four_b':'player.num_errors_q_four_b_split',
      'player.num_errors_q_four_c':'player.num_errors_q_four_c_split',
      'player.num_errors_q_four_d':'player.num_errors_q_four_d_split'
   }, inplace=True)

   split_and_instrucs_df = pd.merge(treatment_df, instrucs_df[['participant.code','player.comprehension_question_one_blue_split',
                                                               'player.comprehension_question_one_green_split','player.comprehension_question_two_split',
                                                               'player.comprehension_question_three_a_split','player.comprehension_question_three_b_split',
                                                               'player.comprehension_question_four_a_split','player.comprehension_question_four_b_split',
                                                               'player.comprehension_question_four_c_split','player.comprehension_question_four_d_split',
                                                               'player.time_to_answer_treatment_instrucs','player.start_time_treatment_instrucs',
                                                               'player.time_spent_instrucs_treatment','player.time_spent_q_one_treatment',
                                                               'player.time_spent_q_two_treatment','player.time_spent_q_three_treatment',
                                                               'player.time_spent_q_four_treatment','player.num_errors_q_one_blue_split',
                                                               'player.num_errors_q_one_green_split', 'player.num_errors_q_two_split',
                                                               'player.num_errors_q_three_a_split','player.num_errors_q_three_b_split',
                                                               'player.num_errors_q_four_a_split','player.num_errors_q_four_b_split',
                                                               'player.num_errors_q_four_c_split','player.num_errors_q_four_d_split'
   ]],on='participant.code')

   split_and_instrucs_df.rename(columns={
       'player.payoff':'player.payoff_treatment',
       'player.start_time':'player.start_time_treatment',
       'player.time_spent_results':'player.time_spent_results_treatment',
       'player.time_spent_cumulative_results':'player.time_spent_cumulative_results_treatment',
       'group.id_in_subsession': 'group.id_in_subsession_treatment',
       'subsession.round_number': 'subsession.round_number_treatment'
    })
   
   split_and_instrucs_df['Shared'] = False
   split_and_instrucs_df['Split'] = True
   split_and_instrucs_df['Single'] = False

   return split_and_instrucs_df


# ====================================================================================================================
# Merge Single DF with treatment Instrucs & Comp Qs relevent columns 
# ====================================================================================================================


def single_merge_game_and_instrucs(treatment_df: pd.DataFrame, instrucs_df: pd.DataFrame):
   """
   Combine the single app and its corresponding instructions data

   :param treatment_df: treatment app dataframe
   :param instrucs_df: treatment instructions dataframe
   :return treatment_and_instrucs_df: merged df with relevent columns renamed
   """
   #rename potentially problematic column names before merge
   instrucs_df.rename(columns={
      'player.comprehension_question_one':'player.comprehension_question_one_single',
      'player.comprehension_question_two':'player.comprehension_question_two_single',
      'player.comprehension_question_three_a':'player.comprehension_question_three_a_single',
      'player.comprehension_question_three_b':'player.comprehension_question_three_b_single',
      'player.comprehension_question_four_a':'player.comprehension_question_four_a_single',
      'player.comprehension_question_four_b':'player.comprehension_question_four_b_single',
      'player.comprehension_question_four_c':'player.comprehension_question_four_c_single',
      'player.time_to_answer':'player.time_to_answer_treatment_instrucs',
      'player.start_time':'player.start_time_treatment_instrucs',
      'player.time_spent_instrucs':'player.time_spent_instrucs_treatment',
      'player.time_spent_q_one':'player.time_spent_q_one_treatment',
      'player.time_spent_q_two':'player.time_spent_q_two_treatment',
      'player.time_spent_q_three':'player.time_spent_q_three_treatment',
      'player.time_spent_q_four':'player.time_spent_q_four_treatment',
      'player.num_errors_q_one':'player.num_errors_q_one_single',
      'player.num_errors_q_two':'player.num_errors_q_two_single',
      'player.num_errors_q_three_a':'player.num_errors_q_three_a_single',
      'player.num_errors_q_three_b':'player.num_errors_q_three_b_single',
      'player.num_errors_q_four_a':'player.num_errors_q_four_a_single',
      'player.num_errors_q_four_b':'player.num_errors_q_four_b_single',
      'player.num_errors_q_four_c':'player.num_errors_q_four_c_single'
   },inplace=True)

   single_and_instrucs_df = pd.merge(treatment_df, instrucs_df[['participant.code','player.comprehension_question_one_single',
                                                                'player.comprehension_question_two_single','player.comprehension_question_three_a_single',
                                                                'player.comprehension_question_three_b_single', 'player.comprehension_question_four_a_single',
                                                                'player.comprehension_question_four_b_single','player.comprehension_question_four_c_single',
                                                                'player.time_to_answer_treatment_instrucs', 'player.start_time_treatment_instrucs',
                                                                'player.time_spent_instrucs_treatment','player.time_spent_q_one_treatment',
                                                                'player.time_spent_q_two_treatment','player.time_spent_q_three_treatment',
                                                                'player.time_spent_q_four_treatment','player.num_errors_q_one_single',
                                                                'player.num_errors_q_two_single','player.num_errors_q_three_a_single',
                                                                'player.num_errors_q_three_b_single','player.num_errors_q_four_a_single',
                                                                'player.num_errors_q_four_b_single','player.num_errors_q_four_c_single']],
                                     on='participant.code')
   
   single_and_instrucs_df.rename(columns={
       'player.payoff':'player.payoff_treatment',
       'player.start_time':'player.start_time_treatment',
       'player.time_spent_results':'player.time_spent_results_treatment',
       'player.time_spent_cumulative_results':'player.time_spent_cumulative_results_treatment',
       'group.id_in_subsession': 'group.id_in_subsession_treatment',
       'subsession.round_number': 'subsession.round_number_treatment'
    })
   
   single_and_instrucs_df['Shared'] = False
   single_and_instrucs_df['Split'] = False
   single_and_instrucs_df['Single'] = True

   return single_and_instrucs_df


# ====================================================================================================================
# Combine all three treatment dfs into a mega df of the treatment data
# ====================================================================================================================


def gen_treatment_all_df(single_df: pd.DataFrame, split_df: pd.DataFrame, shared_df: pd.DataFrame):
   """
   Make the megaladon data frame from all treatments

   :param single_df: Instrucs and app data set for single group pgg
   :param split_df: instruc and app data set for multi-group split pgg
   :param shared: instruc and app data set for multi-group shared pgg
   :return all_treatment_df: the mega dataframe for all treatment related apps 
   """
   all_treatment_df = pd.concat([single_df, split_df, shared_df], axis=0, keys = ['single','split','shared'])
   return all_treatment_df
