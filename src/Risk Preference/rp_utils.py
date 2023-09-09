"""
Functions for 
    A) counting and storing the number of choice 'A's of each subject across all sessions
    B) Produce and store the risk estimation, r, for each subject across all sessions
        i) This r is an interval for the time being (Same as Holt and Laury 2002 [since 
            we have the same switching points as them, and I assume the same utility function]) 
    C) Risk preference classifications (names from Holt and Laury 2002)
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd, plt, np


# ====================================================================================================================
# Count Num_Safe
# ====================================================================================================================


def count_num_safe(df: pd.DataFrame):
    """
    Counts the number of times that the subject chose the safe lottery and returns this as a new column 
    to the existing dataframe

    :param df: the Risk Preference data frame
    :return df: the Risk Preference data frame with the added column counting num_times_A
    """
    # Specify the columns to look for the 'A' selection of subjects
    columns_to_search = ['player.lottery_b_one', 'player.lottery_b_two', 
                         'player.lottery_b_three', 'player.lottery_b_four',
                         'player.lottery_b_five', 'player.lottery_b_six',
                         'player.lottery_b_seven', 'player.lottery_b_eight',
                         'player.lottery_b_nine', 'player.lottery_b_ten']
    # Value to look for | Choice A (safe choice) encoded as 1
    value_to_count = 1 
    # Perform the count operation and save as a new column
    df['player.num_safe_choice'] = df[columns_to_search].apply(lambda row: (row == value_to_count).sum(), axis=1)
    return df


# ====================================================================================================================
# Assign upper-bound for risk estimation (Holt and Laury 2002 values)
# ====================================================================================================================


def risk_estimation_bounds(df: pd.DataFrame, risk_estimation_lower_dict: dict, risk_estimation_upper_dict: dict):
    """
    Attaches a new column containing the upper bound of the risk estimate to the df from the previously found counts

    :param df: Risk Preference data frame
    :param risk_estimation_lower__dict: dictionary containing key == num_safe_choice with value == risk estimate lower bound
    :param risk_estimation_upper__dict: dictionary containing key == num_safe_choice with value == risk estimate upper bound
    :return df: Risk preference data frame with this upper bound
    """
    df['player.risk_estimate_lower_bound'] = df['player.num_safe_choice'].map(risk_estimation_lower_dict)
    df['player.risk_estimate_upper_bound'] = df['player.num_safe_choice'].map(risk_estimation_upper_dict)
    return df


# ====================================================================================================================
# Risk Preference Classifications
# ====================================================================================================================


def assign_risk_preference_classifications(df: pd.DataFrame, risk_classifications_dict: dict):
    """_summary_

    :param df: Risk Preference data frame
    :param risk_classifications_dict: dictionary containing risk 'titles' as labeled by Holt and Laury (2002)
    :return df: Risk Pref df + new column with classifcation
    """
    df['player.risk_preference_classification'] = df['player.num_safe_choice'].map(risk_classifications_dict)
    return df


# ====================================================================================================================
# Summary Statistics on Risk Preference Classifcations // Num safe
# ====================================================================================================================

def gen_rp_summary_statistics_dict(df: pd.DataFrame):
    """
    Generates the summary statistics for the Risk Preference dataset on the num_safe counts 

    :param df: Risk Preference dataframe
    :return: dictionary with the summary statistics 
    """
    min_val = df['player.num_safe_choice'].min()
    max_val = df['player.num_safe_choice'].max()
    range_val = min_val - max_val
    mean_val = df['player.num_safe_choice'].mean()
    median_val = df['player.num_safe_choice'].median()
    mode_val = df['player.num_safe_choice'].mode().iloc[0]  # Taking the first mode in case there are multiple
    # IQR
    Q1 = df['player.num_safe_choice'].quantile(0.25)
    Q3 = df['player.num_safe_choice'].quantile(0.75)
    IQR = Q3 - Q1

    std_val = df['player.num_safe_choice'].std()
    return {
        'min_val': min_val,
        'max_val': max_val,
        'range_val': range_val,
        'mean_val': mean_val,
        'median_val': median_val,
        'mode_val': mode_val,
        'IQR': IQR,
        'std_val': std_val
    }


# ====================================================================================================================
# Bar graph and Histogram // Num safe
# ====================================================================================================================


def gen_bar_graph_rp(df: pd.DataFrame):
    """
    Generates a bar graph for the Risk Preference data frame

    :param df: Risk Preference dataframe
    """
    # Count frequency of each unique value
    value_counts=df['player.num_safe_choice'].value_counts().sort_index()

    # Creat bar plot
    plt.bar(value_counts.index, value_counts.values)

    # Add labels and title
    plt.xlabel('num_safe_choice')
    plt.ylabel('Count')
    plt.title('Count of Scores')

    plt.yticks(np.arange(0, value_counts.values.max() + 1, 1))


    # Show the plot
    plt.show()
