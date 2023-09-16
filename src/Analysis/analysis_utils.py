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
    """_summary_

    :param df: _description_
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
    """_summary_

    :param df: _description_
    :param treatment: _description_
    """
    first_period_df = df[df['subsession.round_number'] == 1]

    avg_first_period_investment_dict = gen_avg_alt(first_period_df, treatment)
    return avg_first_period_investment_dict

def gen_first_period_list(df: pd.DataFrame):
    """_summary_

    :param df: _description_
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
    """_summary_

    :param df: _description_
    :param treatment: _description_
    """
    last_round = df['subsession.round_number'].max()

    if treatment == 'split' or treatment == 'shared':
        blue_investment_dict, green_investment_dict, treatment_avg = {}, {}, {}
        for i in range(1, last_round + 1):
            period_df = df[df['subsession.round_number'] == i]
            blue_grouped_avg_df = period_df.groupby('pgg_treatment_applied')['player.blue_group_investment'].mean()
            green_grouped_avg_df = df.groupby('pgg_treatment_applied')['player.green_group_investment'].mean()

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
    """_summary_

    :param singleAvg: _description_
    :param splitAvg: _description_
    :param sharedAvg: _description_
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
    plt.title('Avg Investment per Treatment in Each Period (Both Groups)')
    plt.legend()
    plt.show()


# ====================================================================================================================
# Average Investments 1-5, 6-10, 11-15, 16-20
# ====================================================================================================================


def gen_invest_subsets(treatment_avg_per_period: dict):
    """_summary_

    :param treatment_avg_per_period: _description_
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
    """_summary_

    :param df: _description_
    :param treatment: _description_
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
    """_summary_

    :param df: _description_
    """
    single_per_participant = gen_avg_invest_per_participant(df, 'single')

    split_per_participant = gen_avg_invest_per_participant(df, 'split')

    shared_per_participant = gen_avg_invest_per_participant(df, 'shared')

    return single_per_participant, split_per_participant, shared_per_participant