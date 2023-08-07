"""
Construct the means to be compared in the power analysis and standard deviation | For first 5 periods
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================

from constants import pd
from constants import np


# ====================================================================================================================
# Construct Averages
# ====================================================================================================================


def gen_investment_avgs_per_period(dataframe: np.ndarray, shared: bool):
  """
  generates the average investment in a given period across both groups and within each group (of type blue / green)

  :param dataframe: the data frame containing data from the shared endowment
  :param shared: boolean 1 if the treatment is shared; otherwise 0
  :return: 3 dictionaries with the average investment to 'blue' groups, 'green' groups, and across both (both is relevant for this analysis)
  """
  last_round = dataframe['subsession.round_number'].max()
  blue_investment_dict, green_investment_dict, treatment_avg = {}, {}, {}

  for i in range(1, last_round + 1):
    condition1 = dataframe['session.is_shared'] == True
    condition2 = dataframe['subsession.round_number'] == i
    blue_investment_dict[f'blue_period_{i}_avg'] = dataframe.loc[condition1 & condition2, 'player.blue_group_investment'].mean()
    green_investment_dict[f'green_period_{i}_avg'] = dataframe.loc[condition1 & condition2, 'player.green_group_investment'].mean()
    treatment_avg[f'period_{i}'] = (blue_investment_dict[f'blue_period_{i}_avg'] + green_investment_dict[f'green_period_{i}_avg']) / 2
  return blue_investment_dict, green_investment_dict, treatment_avg


def gen_investment_avgs_first_five_periods(dataframe: np.ndarray, shared: bool):
  """
  Restrict ourself to comparisons of the first 5 periods as this is what FFG (2013) reports a mean for and serves as our power analysis

  :param dataframe: the data frame containing data from the shared endowment
  :param shared: boolean 1 if the treatment is shared; otherwise 0
  :return: the average investment over the first 5 periods as a number, and then as a percent of the endowment subjects received (20 points).
  """
  blue_dict, green_dict, both_dict = gen_investment_avgs_per_period(dataframe, shared)
  keys_1_to_5 = ['period_1','period_2','period_3','period_4','period_5']
  subset_1_to_5 =  [both_dict[key] for key in keys_1_to_5]
  avg_invest_1_to_5 = sum(subset_1_to_5) / len(subset_1_to_5)
  avg_invest_1_to_5_as_perc = avg_invest_1_to_5 / 20
  return avg_invest_1_to_5, avg_invest_1_to_5_as_perc


def average_investment(df: np.ndarray):
  """
  To construct the standard deviation, I need one level of less abstraction. For this I take the average of each subjects investment in the first 5 periods

  :param df: the data frame containing data from the shared endowment
  :return: creates a new dataframe that displays each subjects average investment over the first 5 periods of play
  """
  # Filter rows for the first 5 periods
  df = df[df['subsession.round_number'] <= 5]

  # Group by subject and calculate the mean for Green and Blue investments
  avg_investments = df.groupby('participant.code')[['player.green_group_investment', 'player.blue_group_investment']].mean().reset_index()
    
  # Rename columns
  avg_investments.columns = ['participant.code', 'player.average_Green_investment', 'player.average_Blue_investment']
    
  # avg across both groups
  avg_investments['player.average_period_1_to_5_invest'] = (avg_investments['player.average_Green_investment'] + avg_investments['player.average_Blue_investment']) / 2

  # As percent of endowment
  avg_investments['player.avg_invest_percent_of_endowment'] = avg_investments['player.average_period_1_to_5_invest'] / 20

  return avg_investments


# ====================================================================================================================
# Construct Standard Deviation
# ====================================================================================================================


def gen_standard_deviation(average_investment_df: np.ndarray):
  """
  Generate the standard deviation with the data points gathered for each subject regarding their investment in the first 5 periods

  :param average_investment_df: a dataframe containing the player level information for each players average first 5 period investment
  :return: the standard deviation of the averages, and then the standard deviation of the percents of endowment invested
  """
  invest_stdev = average_investment_df['player.average_period_1_to_5_invest'].std()
  invest_stdev_as_perc = average_investment_df['player.avg_invest_percent_of_endowment'].std()
  return invest_stdev, invest_stdev_as_perc