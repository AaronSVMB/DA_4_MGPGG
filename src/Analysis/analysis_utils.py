"""
Functions for MGPGG analysis, statistical tests, visuals, etc.
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================

from constants import pd
from constants import plt

# ====================================================================================================================
# Average Investments
# ====================================================================================================================

    
def gen_avg_alt(df: pd.DataFrame, treatment: str):
    """
    Generates averages and standard deviations for investments for each treatment

    :param df: mgpggdf all apps
    :param treatment: str value of 'single', 'split', or 'shared'
    :return: dictionary with treatment name, average investments, and standard deviations
    """
    if treatment == 'split' or treatment == 'shared':
        blue_grouped_avg_df = df.groupby('pgg_treatment_applied')['player.blue_group_investment'].mean()
        blue_grouped_std_df = df.groupby('pgg_treatment_applied')['player.blue_group_investment'].std()
        

        green_grouped_avg_df = df.groupby('pgg_treatment_applied')['player.green_group_investment'].mean()
        green_grouped_std_df = df.groupby('pgg_treatment_applied')['player.green_group_investment'].std()

        filtered_df = df[df['pgg_treatment_applied'].isin([treatment])]

        # Combine the two columns into a single Series from the filtered DataFrame
        combined_values = pd.concat([filtered_df['player.blue_group_investment'], filtered_df['player.green_group_investment']])

        # Calculate the standard deviation of the combined values
        std_combined = combined_values.std()

        avg_across = (blue_grouped_avg_df.loc[treatment] + green_grouped_avg_df[treatment] ) 

        avg_investment_dict = {'treatment': treatment,
                               'avg_blue_investment': blue_grouped_avg_df.loc[treatment], 'std_blue': blue_grouped_std_df.loc[treatment],
                               'avg_green_investment': green_grouped_avg_df.loc[treatment], 'std_green': green_grouped_std_df.loc[treatment],
                               'avg_both': avg_across, 'std_both': std_combined}
        
    else:
        average_investment = df.groupby('pgg_treatment_applied')['player.investment'].mean()
        investment_std = df.groupby('pgg_treatment_applied')['player.investment'].std()
        avg_investment_dict = {'treatment': treatment,
                               'average_investment': average_investment.loc[treatment],
                               'investment_std': investment_std.loc[treatment]}
    return avg_investment_dict 

    
def gen_avg_invest_per_group_per_treatment_list(df : pd.DataFrame):
    """generates average investments for all treatments. saves as a list of dictionaries

    :param df: mgpggdf all apps
    """
    # Single
    single_avg = gen_avg_alt(df, 'single')
    # Split
    split_avg = gen_avg_alt(df, 'split')
    # Shared 
    shared_avg = gen_avg_alt(df, 'shared')
    avg_list = [single_avg, split_avg, shared_avg]
    return avg_list


# ====================================================================================================================
# Average First Period Investment Investments
# ====================================================================================================================


def gen_avg_first_period_invest_per_treatment(df: pd.DataFrame, treatment: str):
    """Generates average first period investment for a specified treatment

    :param df: mgpggdf all apps
    :param treatment: str value of 'single', 'split', or 'shared'
    """
    first_period_df = df[df['subsession.round_number'] == 1]

    avg_first_period_investment_dict = gen_avg_alt(first_period_df, treatment)
    return avg_first_period_investment_dict

def gen_first_period_list(df: pd.DataFrame):
    """generates all average first period investments for all 3 treatments. saves as a list of dictionaries

    :param df: mgpggdf all apps
    """
    # Single
    single_avg = gen_avg_first_period_invest_per_treatment(df, 'single')
    # Split
    split_avg = gen_avg_first_period_invest_per_treatment(df, 'split')
    # Shared 
    shared_avg = gen_avg_first_period_invest_per_treatment(df, 'shared')
    avg_list = [single_avg, split_avg, shared_avg]
    return avg_list


# ====================================================================================================================
# Average Investments Per Period
# ====================================================================================================================


def gen_investment_avg_invest_per_period(df: pd.DataFrame, treatment: str):
    """generates average investment in each period for a specified treatment

    :param df: mgpggdf all apps
    :param treatment: str value of 'single', 'split', or 'shared'
    """
    last_round = df['subsession.round_number'].max()

    if treatment == 'split' or treatment == 'shared':
        blue_investment_dict, green_investment_dict, treatment_avg = {}, {}, {}
        for i in range(1, last_round + 1):
            period_df = df[df['subsession.round_number'] == i]
            blue_grouped_avg_df = period_df.groupby('pgg_treatment_applied')['player.blue_group_investment'].mean()
            green_grouped_avg_df = period_df.groupby('pgg_treatment_applied')['player.green_group_investment'].mean()

            blue_investment_dict[f'blue_period_{i}_avg'] = blue_grouped_avg_df.loc[treatment]
            green_investment_dict[f'green_period_{i}_avg'] = green_grouped_avg_df.loc[treatment]
            treatment_avg[f'period_{i}'] = blue_grouped_avg_df.loc[treatment] + green_grouped_avg_df.loc[treatment]
        return blue_investment_dict, green_investment_dict, treatment_avg
    else:
         treatment_avg = {}
         for i in range(1, last_round + 1):
            period_df = df[df['subsession.round_number'] == i]
            average_investment = period_df.groupby('pgg_treatment_applied')['player.investment'].mean()
            treatment_avg[f'period_{i}'] = average_investment[treatment]
    return treatment_avg


def gen_avg_invest_plots(df: pd.DataFrame ,singleAvg: dict, splitAvg: dict, sharedAvg: dict):
    """generates a line graph with period on the x-axis and average investment as the y. plots all 3 treatments

    :param singleAvg: single treatment avg invest schedule
    :param splitAvg: split treatment avg invest schedule
    :param sharedAvg: shared treatment avg invest schedule
    """
    last_round = df['subsession.round_number'].max()
    x_values = [i for i in range(1, last_round + 1)]

    ySingle = [value for value in singleAvg.values()]
    ySplit = [value for value in splitAvg.values()]
    yShared = [value for value in sharedAvg.values()]

    plt.plot(x_values, ySingle, label='single', color='r', marker='o')
    plt.plot(x_values, ySplit, label='split', color='g', marker='s')
    plt.plot(x_values, yShared, label='shared', color='b', marker='^')

    plt.xlabel('Periods')
    plt.ylabel('Avg Investment to Group Joint Account(s)')
    plt.ylim(0, 20)
    plt.title('Avg Investment per Treatment in Each Period (Both Groups)')
    plt.legend()
    plt.show()


# ====================================================================================================================
# Average Investments 1-5, 6-10, 11-15, 16-20
# ====================================================================================================================


def gen_invest_subsets(treatment_avg_per_period: dict):
    """generates sub set ranges 1, 2-10, and 11-20 of average investments

    :param treatment_avg_per_period: avg investment schedule for a selected treatment
    """
    avgs_period_groupings_dict = {}
    avgs_period_groupings_dict['period_1'] = treatment_avg_per_period['period_1']

    keys_2_to_10 = ['period_2','period_3','period_4','period_5','period_6','period_7','period_8','period_9','period_10']
    subset_2_to_10 =  [treatment_avg_per_period[key] for key in keys_2_to_10]

    avgs_period_groupings_dict['period_2_to_10'] = sum(subset_2_to_10) / len(subset_2_to_10)

    keys_11_to_20 = ['period_11','period_12','period_13','period_14','period_15','period_16','period_17','period_18','period_19','period_20']
    subset_11_to_20 =  [treatment_avg_per_period[key] for key in keys_11_to_20]

    avgs_period_groupings_dict['period_11_to_20'] = sum(subset_11_to_20) / len(subset_11_to_20)

    return avgs_period_groupings_dict


# ====================================================================================================================
# Average Investments per individual across all groups, periods
# ====================================================================================================================


def gen_avg_invest_per_participant(df: pd.DataFrame, treatment: str):
    """generate average investment for each participant across 20 periods

    :param df: mgpggdf all apps
    :param treatment: str value of 'single', 'split', or 'shared'
    """
    if treatment == 'single':
        single_df = df[df['pgg_treatment_applied'] == treatment]
        average_investment_per_participant = single_df.groupby('participant.code')['player.investment'].mean()
    elif treatment == 'split':
        split_df = df[df['pgg_treatment_applied'] == treatment]
        average_invest_blue = split_df.groupby('participant.code')['player.blue_group_investment'].mean()
        average_invest_green = split_df.groupby('participant.code')['player.green_group_investment'].mean()
        average_investment_per_participant =  average_invest_blue + average_invest_green
    else:
        shared_df = df[df['pgg_treatment_applied'] == treatment]
        average_invest_blue = shared_df.groupby('participant.code')['player.blue_group_investment'].mean()
        average_invest_green = shared_df.groupby('participant.code')['player.green_group_investment'].mean()
        average_investment_per_participant =  average_invest_blue + average_invest_green

    return average_investment_per_participant


def gen_avg_investment_per_participant_all_treatments(df: pd.DataFrame):
    """generates average investment per subject across all 20 periods for all 3 treatments

    :param df: mgpggdf all apps
    """
    single_per_participant = gen_avg_invest_per_participant(df, 'single')

    split_per_participant = gen_avg_invest_per_participant(df, 'split')

    shared_per_participant = gen_avg_invest_per_participant(df, 'shared')

    return single_per_participant, split_per_participant, shared_per_participant


# ====================================================================================================================
# Gender Difference 
# ====================================================================================================================


def gen_gender_split(df: pd.DataFrame):
    """generate average investment lists for each participant split by gender

    :param df: mgpggdf all apps
    """
    # Single series for female, then male
    single_df = df[df['pgg_treatment_applied'] == 'single']
    single__female_df = single_df[single_df['player.gender'] == 2]
    average_investment_per_participant_female_single = single__female_df.groupby('participant.code')['player.investment'].mean()

    single__male_df = single_df[single_df['player.gender'] == 1]
    average_investment_per_participant_male_single = single__male_df.groupby('participant.code')['player.investment'].mean()

    # Multi series for female then male
    multi_df = df[df['pgg_treatment_applied'] != 'single' ]
    multi__female_df = multi_df[multi_df['player.gender'] == 2]
    average_invest_blue_female = multi__female_df.groupby('participant.code')['player.blue_group_investment'].mean()
    average_invest_green_female = multi__female_df.groupby('participant.code')['player.green_group_investment'].mean()
    average_investment_per_participant_female_multi =  average_invest_blue_female + average_invest_green_female

    multi__male_df = multi_df[multi_df['player.gender'] == 1]
    average_invest_blue_male = multi__male_df.groupby('participant.code')['player.blue_group_investment'].mean()
    average_invest_green_male = multi__male_df.groupby('participant.code')['player.green_group_investment'].mean()
    average_investment_per_participant_male_multi =  average_invest_blue_male + average_invest_green_male

    female_df = pd.concat([average_investment_per_participant_female_single, average_investment_per_participant_female_multi])
    male_df = pd.concat([average_investment_per_participant_male_single, average_investment_per_participant_male_multi])

    return female_df, male_df
    
    
# ====================================================================================================================
# DAta prep, regressions
# ====================================================================================================================

def gen_data_panel_ols(df: pd.DataFrame, indices: list, depVar: str, indepVar):
    """_summary_

    :param df: _description_
    :param indices: _description_
    :param depVar: _description_
    :param indepVar: _description_
    """
    #TODO fix 
    depVarList = list(depVar)
    columns_to_keep = indices + depVarList + indepVar
    df = df.loc[:, columns_to_keep ]
    return df 