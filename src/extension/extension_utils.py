"""
Data cleaning and reading code for Questionnaire Data
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd
from constants import plt
from constants import stats
from scipy.stats import ttest_ind
from scipy.stats import mannwhitneyu
from scipy.stats import wilcoxon
import statsmodels.stats.multitest as smm

# ====================================================================================================================
# Data Reading and Cleaning
# ====================================================================================================================

def extension_reading_and_cleaning(filename:str):
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


def extension_merge_game_and_instrucs(extension_df: pd.DataFrame, instrucs_df: pd.DataFrame):
    extension_game_and_instrucs_df = pd.merge(extension_df, instrucs_df[['participant.code','player.comprehension_question_one',
                                                                         'player.comprehension_question_two', 'player.comprehension_question_two_point_five',
                                                                         'player.comprehension_question_three_a', 'player.comprehension_question_three_b',
                                                                         'player.comprehension_question_four_a', 'player.comprehension_question_four_b',
                                                                         'player.comprehension_question_four_c', 'player.comprehension_question_four_d',
                                                                         'player.time_spent_instrucs', 'player.time_spent_q_one',
                                                                         'player.time_spent_q_two', 'player.time_spent_q_two_point_five',
                                                                         'player.time_spent_q_three', 'player.time_spent_q_four',
                                                                         'player.num_errors_q_one', 'player.num_errors_q_two', 
                                                                         'player.num_errors_q_two_point_five', 'player.num_errors_q_three_a',
                                                                         'player.num_errors_q_three_b', 'player.num_errors_q_four_a',
                                                                         'player.num_errors_q_four_b', 'player.num_errors_q_four_c',
                                                                         'player.num_errors_q_four_d']],
                                                                           on='participant.code')
    return extension_game_and_instrucs_df


def extension_merge_game_and_survey(extension_df: pd.DataFrame, survey_df: pd.DataFrame):
    extension_game_and_survey = pd.merge(extension_df, survey_df[['participant.code', 'player.password_to_start', 'player.gender', 'player.age', 'player.grade',
                                                                  'player.major', 'player.risk', 'player.compare_groups', 'player.personal_versus_group',
                                                                  'player.change', 'player.bot_number_blue', 'player.bot_level_blue', 'player.bots_pattern_blue',
                                                                  'player.bots_own_blue', 'player.bots_understand_blue', 'player.bot_number_green', 'player.bot_level_green',
                                                                  'player.bots_pattern_green', 'player.bots_own_green', 'player.bots_understand_green',
                                                                  'player.reason_group', 'player.reason_conditional', 'player.reason_experiment', 'player.reason_adjust',
                                                                  'player.reason_future_rounds', 'player.decision_style_facts', 'player.decision_style_feelings', 'player.decision_style_family',
                                                                  'player.decision_style_friend', 'player.clarity', 'player.suggestions', 'player.time_spent_survey_one',
                                                                  'player.time_spent_survey_bots', 'player.time_spent_survey_two', 'player.time_spent_survey_three', 'player.time_spent_survey_four']],
                                         on = 'participant.code')
    return extension_game_and_survey
    

# =================================================================================================================
# Basic Average
# ====================================================================================================================


def gen_avg_investments(df: pd.DataFrame):
    """
    Generates averages and standard deviations for investments for each treatment
    and for cases when 'blue_green' is True or False.

    :param df: DataFrame with all apps
    :return: dictionary with treatment name, average investments, and standard deviations
    """
    # Calculate averages and standard deviations for the 'blue_group'
    blue_grouped_avg_df = df['player.blue_group_investment'].mean()
    blue_grouped_std_df = df['player.blue_group_investment'].std()

    # Calculate averages and standard deviations for the 'green_group'
    green_grouped_avg_df = df['player.green_group_investment'].mean()
    green_grouped_std_df = df['player.green_group_investment'].std()

    # Calculate averages and standard deviations for the cases where 'blue_green' is True
    blue_true_avg = df[df['blue_green']]['player.blue_group_investment'].mean()
    blue_true_std = df[df['blue_green']]['player.blue_group_investment'].std()
    green_true_avg = df[df['blue_green']]['player.green_group_investment'].mean()
    green_true_std = df[df['blue_green']]['player.green_group_investment'].std()

    # Calculate averages and standard deviations for the cases where 'blue_green' is False
    blue_false_avg = df[~df['blue_green']]['player.blue_group_investment'].mean()
    blue_false_std = df[~df['blue_green']]['player.blue_group_investment'].std()
    green_false_avg = df[~df['blue_green']]['player.green_group_investment'].mean()
    green_false_std = df[~df['blue_green']]['player.green_group_investment'].std()

    # Combine the results into a dictionary
    avg_investment_dict = {
        'treatment': 'shared',
        'avg_blue_investment': blue_grouped_avg_df, 
        'std_blue': blue_grouped_std_df,
        'avg_green_investment': green_grouped_avg_df, 
        'std_green': green_grouped_std_df,
        'avg_blue_true': blue_true_avg, 
        'std_blue_true': blue_true_std,
        'avg_green_true': green_true_avg, 
        'std_green_true': green_true_std,
        'avg_blue_false': blue_false_avg, 
        'std_blue_false': blue_false_std,
        'avg_green_false': green_false_avg, 
        'std_green_false': green_false_std
    }

    return avg_investment_dict


# =================================================================================================================
# One Session Plot of CC group vs. FF group investment from HUMAN subjects
# ====================================================================================================================


def calculate_and_plot_averages(df):
    # Filter the DataFrame based on 'blue_green' being True or False
    df_true = df[df['blue_green']]
    df_false = df[~df['blue_green']]

    # Calculate the mean investments for the 'better' and 'worse' groups for both True and False cases
    # across all sessions
    better_group_averages_true = df_true[df_true['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.green_group_investment'].mean() \
                                + df_true[df_true['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.blue_group_investment'].mean()

    worse_group_averages_true = df_true[df_true['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.blue_group_investment'].mean() \
                               + df_true[df_true['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.green_group_investment'].mean()

    better_group_averages_false = df_false[df_false['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.green_group_investment'].mean() \
                                 + df_false[df_false['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.blue_group_investment'].mean()

    worse_group_averages_false = df_false[df_false['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.blue_group_investment'].mean() \
                                + df_false[df_false['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.green_group_investment'].mean()

    # Plotting
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20, 5))

    # Plot for when 'blue_green' is True
    axes[0].plot(better_group_averages_true.index, better_group_averages_true.values, label='Better Group B-G', marker='o')
    axes[0].plot(worse_group_averages_true.index, worse_group_averages_true.values, label='Worse Group B-G', marker='x')
    axes[0].set_title('Group Average Investments with Blue-Green Screen Order')
    axes[0].set_xlabel('Period')
    axes[0].set_ylabel('Average Investment')
    axes[0].set_xlim(0, 20)
    axes[0].set_ylim(0, 20)
    axes[0].set_xticks(range(0, 21))
    axes[0].set_yticks(range(0, 21))
    axes[0].legend()
    axes[0].grid(True)

    # Plot for when 'blue_green' is False
    axes[1].plot(better_group_averages_false.index, better_group_averages_false.values, label='Better Group G-B', marker='o')
    axes[1].plot(worse_group_averages_false.index, worse_group_averages_false.values, label='Worse Group G-B', marker='x')
    axes[1].set_title('Group Average Investments with Green-Blue Screen Order')
    axes[1].set_xlabel('Period')
    axes[1].set_ylabel('Average Investment')
    axes[1].set_xlim(0, 20)
    axes[1].set_ylim(0, 20)
    axes[1].set_xticks(range(0, 21))
    axes[1].set_yticks(range(0, 21))
    axes[1].legend()
    axes[1].grid(True)

    plt.tight_layout()
    plt.show()


# =================================================================================================================
# Content for TTest & non-param
# ====================================================================================================================

def calculate_averages(df):
    # Group by round number and calculate the mean investments for each group
    better_group_averages = df[df['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.green_group_investment'].mean() \
                            + df[df['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.blue_group_investment'].mean()

    worse_group_averages = df[df['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.blue_group_investment'].mean() \
                           + df[df['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.green_group_investment'].mean()

    # Return as DataFrames
    return better_group_averages, worse_group_averages


def perform_t_tests(df):
    # Calculate the better and worse group averages for when 'blue_green' is True
    better_group_averages_true, worse_group_averages_true = calculate_averages(df[df['blue_green'] == True])
    
    # Calculate the better and worse group averages for when 'blue_green' is False
    better_group_averages_false, worse_group_averages_false = calculate_averages(df[df['blue_green'] == False])
    
    # Perform the t-tests
    # We assume the data is independent between the two treatments ('blue_green' True vs False)
    # and we're comparing the means of the better and worse group averages for each treatment
    t_test_better = ttest_ind(
        better_group_averages_true, 
        better_group_averages_false, 
        equal_var=False
    )
    t_test_worse = ttest_ind(
        worse_group_averages_true, 
        worse_group_averages_false, 
        equal_var=False
    )
    
    # Return the t-test results
    return {
        't_test_better': t_test_better, 
        't_test_worse': t_test_worse
    }


def perform_non_parametric_tests(df):
    # Calculate the better and worse group averages for when 'blue_green' is True
    better_group_averages_true, worse_group_averages_true = calculate_averages(df[df['blue_green'] == True])
    
    # Calculate the better and worse group averages for when 'blue_green' is False
    better_group_averages_false, worse_group_averages_false = calculate_averages(df[df['blue_green'] == False])
    
    # Perform the Mann-Whitney U test
    # We assume the data is independent between the two treatments ('blue_green' True vs False)
    # and we're comparing the distributions of the better and worse group averages for each treatment
    u_test_better = mannwhitneyu(
        better_group_averages_true, 
        better_group_averages_false, 
        alternative='two-sided'
    )
    u_test_worse = mannwhitneyu(
        worse_group_averages_true, 
        worse_group_averages_false, 
        alternative='two-sided'
    )
    
    # Return the test results
    return {
        'u_test_better': {'statistic': u_test_better.statistic, 'p_value': u_test_better.pvalue}, 
        'u_test_worse': {'statistic': u_test_worse.statistic, 'p_value': u_test_worse.pvalue}
    }


# =================================================================================================================
# Plot combined data
# ====================================================================================================================


def plot_averages_all(df):
    # Calculate the mean investments for the 'better' and 'worse' groups across all sessions
    better_group_averages = df[df['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.green_group_investment'].mean() \
                            + df[df['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.blue_group_investment'].mean()

    worse_group_averages = df[df['player.id_in_group'].isin([1, 2, 3, 4])].groupby('subsession.round_number')['player.blue_group_investment'].mean() \
                           + df[df['player.id_in_group'].isin([5, 6, 7, 8])].groupby('subsession.round_number')['player.green_group_investment'].mean()

    # Plotting
    plt.figure(figsize=(10, 5))

    # Plot the better group averages
    plt.plot(better_group_averages.index, better_group_averages.values, label='Better Group Average', marker='o')

    # Plot the worse group averages
    plt.plot(worse_group_averages.index, worse_group_averages.values, label='Worse Group Average', marker='x')

    plt.title('Group Averages Across All Data')
    plt.xlabel('Round Number')
    plt.ylabel('Average Investment')
    plt.legend()
    plt.grid(True)
    plt.show()


# =================================================================================================================
# Compare Rounds – Correct for Multiple Comparisons 
# ====================================================================================================================


def test_investment_difference_by_round_corrected(df):
    # Initialize a list to hold p-values
    p_values = []
    rounds = df['subsession.round_number'].unique()
    
    # Loop through each round
    for round_number in rounds:
        # Filter the DataFrame for the current round
        df_round = df[df['subsession.round_number'] == round_number]

        # Calculate the investments for the 'better' and 'worse' groups
        better_investments = df_round[df_round['player.id_in_group'].isin([1, 2, 3, 4])]['player.green_group_investment'] \
                             + df_round[df_round['player.id_in_group'].isin([5, 6, 7, 8])]['player.blue_group_investment']

        worse_investments = df_round[df_round['player.id_in_group'].isin([1, 2, 3, 4])]['player.blue_group_investment'] \
                            + df_round[df_round['player.id_in_group'].isin([5, 6, 7, 8])]['player.green_group_investment']

        # Perform the Wilcoxon signed-rank test for each round
        # We use a paired test since each subject contributes to both groups
        stat, p = wilcoxon(better_investments, worse_investments)
        p_values.append(p)
    
    # Correct for multiple comparisons using the Benjamini-Hochberg method
    # This controls the False Discovery Rate (FDR)
    reject, p_values_corrected, _, _ = smm.multipletests(p_values, alpha=0.05, method='fdr_bh')
    
    # Combine rounds, p-values, and corrected p-values into a dataframe for better readability
    results_df = pd.DataFrame({
        'Round': rounds,
        'P-Value': p_values,
        'P-Value Corrected': p_values_corrected,
        'Reject Null': reject
    })

    return results_df


# =================================================================================================================
# Encode 'better' and 'worse' group decisions for EXTENSION instead of arbitrary 'blue' and 'green'
# ====================================================================================================================



def encode_group_investments(df):
    # Initialize new columns with default values
    df['player.better_group_investment'] = None
    df['player.worse_group_investment'] = None
    df['better_group'] = None
    df['worse_group'] = None

    # Loop over the DataFrame and apply the logic based on player.id_in_group
    for index, row in df.iterrows():
        if row['player.id_in_group'] in [1, 2, 3, 4]:
            # If player's id is in [1, 2, 3, 4], green is the better group, blue is the worse group
            df.at[index, 'player.better_group_investment'] = row['player.green_group_investment']
            df.at[index, 'player.worse_group_investment'] = row['player.blue_group_investment']
            df.at[index, 'better_group'] = 'green'
            df.at[index, 'worse_group'] = 'blue'
        elif row['player.id_in_group'] in [5, 6, 7, 8]:
            # If player's id is in [5, 6, 7, 8], blue is the better group, green is the worse group
            df.at[index, 'player.better_group_investment'] = row['player.blue_group_investment']
            df.at[index, 'player.worse_group_investment'] = row['player.green_group_investment']
            df.at[index, 'better_group'] = 'blue'
            df.at[index, 'worse_group'] = 'green'

    return df


def encode_additional_group_investments(df):
    # Encode total investments for better/worse group
    df['player.better_group_total_investment'] = df.apply(
        lambda row: row['player.green_group_total_investment'] if row['better_group'] == 'green' else row['player.blue_group_total_investment'], axis=1
    )
    df['player.worse_group_total_investment'] = df.apply(
        lambda row: row['player.blue_group_total_investment'] if row['worse_group'] == 'blue' else row['player.green_group_total_investment'], axis=1
    )

    # Encode bot investments for better/worse group
    df['player.better_group_bot_investment'] = df.apply(
        lambda row: (row['player.green_bot_one_investment'] + row['player.green_bot_two_investment']) if row['better_group'] == 'green' else (row['player.blue_bot_one_investment'] + row['player.blue_bot_two_investment']), axis=1
    )
    df['player.worse_group_bot_investment'] = df.apply(
        lambda row: (row['player.blue_bot_one_investment'] + row['player.blue_bot_two_investment']) if row['worse_group'] == 'blue' else (row['player.green_bot_one_investment'] + row['player.green_bot_two_investment']), axis=1
    )

    return df

