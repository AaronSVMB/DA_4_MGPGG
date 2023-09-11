"""
Data cleaning and reading code for Questionnaire Data
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================

def questionnaire_reading_and_cleaning(filename:str):
    """
    Takes in Questionnaire data from oTree and cleans the data in the follow way

    :param filename: questionnaire data set
    :return dataframe: cleaned df of the questionnaire data set
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


# ====================================================================================================================
# Concat Larry Single and Larry Multi DF
# ====================================================================================================================

def questionnaire_concat_single_and_multi(larry_single_df: pd.DataFrame, larry_multi_df: pd.DataFrame):
    """
    Since we use slightly different variations of survey questions depending on if the MG or the Single treatment
    is in use, I merge the survey apps data from oTree

    :param larry_single_df: survey data from subjects who were in the single group pgg
    :param larry_multi_df: survey data from subjects who were in the multi-shared or multi-split pgg
    :return larry_single_and_multi_df: merged df of the two
    """
    larry_single_and_multi_df = pd.concat([larry_single_df, larry_multi_df[['participant.id_in_session', 'participant.code', 
                                                                          'participant.payoff', 'player.id_in_group',
                                                                          'player.payoff', 'player.password_to_start',
                                                                          'player.gender', 'player.age',
                                                                          'player.grade', 'player.major',
                                                                          'player.risk', 'player.compare_groups',
                                                                          'player.personal_versus_group', 'player.change',
                                                                          'player.reason_own', 'player.reason_group',
                                                                          'player.reason_conditional', 'player.reason_experiment',
                                                                          'player.reason_adjust', 'player.reason_future_rounds',
                                                                          'player.decision_style_facts', 'player.decision_style_feelings',
                                                                          'player.decision_style_family', 'player.decision_style_friend',
                                                                          'player.clarity', 'player.suggestions',
                                                                          'player.start_time', 'player.time_spent_survey_one', 'player.time_spent_survey_two',
                                                                          'player.time_spent_survey_three', 'player.time_spent_survey_four', 'group.id_in_subsession',
                                                                          'subsession.round_number', 'session.code', 'session.is_demo']]],
                                                                          ignore_index=True
                                                                          )
    return larry_single_and_multi_df


# ====================================================================================================================
# Concat larry_both and aaron_survey together
# ====================================================================================================================


def questionnaire_concat_larry_and_aaron(larry_both: pd.DataFrame, aaron_survey: pd.DataFrame):
    """
    Combine the survey questions from larry_both and aaron_survey 

    :param larry_both: Larrys Single and Larry Multi Survey responses
    :param aaron_survey: Aaron's survey responses (1 shared endowment session)
    :return questionnaire_df: All survey question data from all treatments of MGPGG experiments
    """
    questionnaire_all_df = pd.concat([larry_both, aaron_survey[['participant.id_in_session', 'participant.code',
                                                                'participant.payoff', 'player.id_in_group',
                                                                'player.payoff', 'player.password_to_start',
                                                                'player.gender', 'player.age', 'player.grade',
                                                                'player.major', 'player.risk', 'player.reasoning',
                                                                'player.signaling', 'player.decision_style_facts',
                                                                'player.decision_style_feelings', 'player.clarity',
                                                                'player.suggestions', 'player.start_time',
                                                                'player.time_spent_survey_one', 'player.time_spent_survey_two',
                                                                'player.time_spent_survey_three', 'group.id_in_subsession',
                                                                'subsession.round_number', 'session.code', 'session.is_demo']]],
                                                                ignore_index =True
                                                                )
    
    # Rename certain column names to avoid any issues when combining with big data frame

    questionnaire_all_df.rename(columns={
        'player.id_in_group':'player.id_in_group_survey',
        'player.payoff':'player.payoff_survey',
        'player.password_to_start':'player.password_to_start_survey',
        'player.start_time':'player.start_time_survey',
        'group.id_in_subsession':'group_id_in_subsession_survey',
        'subsesion.round_number':'subsession.round_number_survey'
    }, inplace=True)

    return questionnaire_all_df
