"""
Generate the big data set for the MGPGG experiment across all apps.
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Data Merging
# ====================================================================================================================


def gen_mgpgg_df(all_treatment_file: str, all_sm_file: str, 
                 lottery_file: str, questionnaire_file: str):
    """
    Combine cleaned and slightly analyzed data together for big data frame to do treatment analysis, regressions, etc.

    :param all_treatment_file: Combined treatment df (single, split, shared) with intructions and comp q data
    :param all_sm_file:  combined strategy method app and instrucs data | with FGF classifications
    :param lottery_file: subject lottery data with holt laury (2002) classifications
    :param questionnaire_file: combined questionnaire data set with subject responses
    :return mgpgg_df: the data frame storing all multi-group pgg content data across all sessions (to-date)
    """
    # Read sub files into DataFrames
    all_treatment_df = pd.read_csv(all_treatment_file)
    all_sm_df = pd.read_csv(all_sm_file)
    all_sm_df.drop(['participant.id_in_session',
                    'session.code',
                    'session.is_demo',
                    'participant.payoff',
                    'subsession.round_number_sm'], axis=1, inplace=True)
    lottery_df = pd.read_csv(lottery_file)
    lottery_df.drop(['participant.id_in_session',
                    'session.code',
                    'session.is_demo',
                    'participant.payoff',
                    'group.id_in_subsession_lottery',
                    'subsession.round_number_lottery'], axis=1, inplace=True)
    questionnaire_df = pd.read_csv(questionnaire_file)
    questionnaire_df.drop(['participant.payoff',
                           'participant.id_in_session',
                           'session.is_demo',
                           'session.code',
                           'group_id_in_subsession_survey',
                           'subsession.round_number'], axis=1, inplace=True)

    # Turn Sub DataFrames into the MGPGG DF
    treatment_and_sm_df = pd.merge(all_treatment_df, all_sm_df, on='participant.code')
    treatment_sm_and_lottery_df = pd.merge(treatment_and_sm_df, lottery_df, on='participant.code')
    mgpgg_df = pd.merge(treatment_sm_and_lottery_df, questionnaire_df, on='participant.code')

    mgpgg_df.drop(['Shared','Split','Single','Unnamed: 1', 'Unnamed: 0_y', 'Unnamed: 0'], axis=1, inplace=True)
    mgpgg_df.rename(columns={'Unnamed: 0_x':'pgg_treatment_applied'}, inplace=True)
    return mgpgg_df