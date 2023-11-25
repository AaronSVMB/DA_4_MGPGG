"""
Functions that deal with the decisions subjects made in the strategy method portion of the experiment;
(1) their unconditional investment and (2) their conditional investments
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import np, plt


# ====================================================================================================================
# Unconditional Investment Averages
# ====================================================================================================================


def gen_unconditional_investment_avgs(dataframe: np.ndarray):
  """
  generate the average unconditional investment for player across playertypes and
  within them and produces a dictionary

  :param dataframe - strategy method dataframe with all relevant typings
  :return: dictionary with unconditional investment avgs for each player type
  """
  avg_uncon_all_player_types = dataframe['player.unconditional_investment'].mean()
  av_uncon_free_rider = dataframe.loc[dataframe['player.is_freerider'] == True, 'player.unconditional_investment'].mean()
  avg_uncon_conditional_cooperator = dataframe.loc[dataframe['player.is_conditional_cooperator'] == True, 'player.unconditional_investment'].mean()
  avg_uncon_hump_shaped = dataframe.loc[dataframe['player.is_hump_shaped'] == True, 'player.unconditional_investment'].mean()
  avg_uncon_other = dataframe.loc[dataframe['player.is_other'] == True, 'player.unconditional_investment'].mean()
  uncon_invests_avgs_dict = {
      'all_players': avg_uncon_all_player_types,
      'free_riders': av_uncon_free_rider,
      'conditional_cooperators': avg_uncon_conditional_cooperator,
      'hump_shaped': avg_uncon_hump_shaped,
      'others': avg_uncon_other
  }
  return uncon_invests_avgs_dict


# ====================================================================================================================
# Conditional Investment Averages
# ====================================================================================================================


def gen_avg_conditional_investments(dataframe: np.ndarray, col_names: list):
  """
  generates the average conditional investments for each specified group average for all player types

  :param dataframe - strategy method dataframe with all relevant typings
  :param col_names - the relevant columns that contain the conditional investment data for each player
  :return: 
  """
  avg_conditional_investment_all_types = dataframe[col_names].mean()
  avg_conditional_investment_free_rider = dataframe.loc[dataframe['player.is_freerider']== True, col_names].mean()
  avg_conditional_investment_conditional_cooperator = dataframe.loc[dataframe['player.is_conditional_cooperator']==True, col_names].mean()
  avg_conditional_investment_hump_shaped = dataframe.loc[dataframe['player.is_hump_shaped']==True, col_names].mean()
  avg_conditional_investment_other = dataframe.loc[dataframe['player.is_other']==True, col_names].mean()
  conditional_invests_avgs_dict = {
      'all_players': avg_conditional_investment_all_types,
      'free_riders': avg_conditional_investment_free_rider,
      'conditional_cooperators': avg_conditional_investment_conditional_cooperator,
      'hump_shaped': avg_conditional_investment_hump_shaped,
      'others': avg_conditional_investment_other
  }
  return conditional_invests_avgs_dict


def fgf_plot(x_values: list, conditional_investment_dict: dict):
  """
  FGF plot that is in their paper and in the Quercia paper. Plot the avgs by playertype on one graph

  :param x_values - the 0 through 20 for the specified level of group investment
  :param conditional_investment_dict - the investment averages for each player type at specfiic group levels
  :return: xy plot 
  """
  # take the investment schemes as a list 
  all_players_list = conditional_investment_dict['all_players'].tolist()
  free_riders_list = conditional_investment_dict['free_riders'].tolist()
  conditional_cooperators_list = conditional_investment_dict['conditional_cooperators'].tolist()
  hump_shaped_list = conditional_investment_dict['hump_shaped'].tolist()
  others_list = conditional_investment_dict['others'].tolist()

  # lines 
  plt.plot(x_values, all_players_list, label='All Players')
  plt.plot(x_values, free_riders_list, label='Free-riders')
  plt.plot(x_values, conditional_cooperators_list, label='Conditional Cooperators')
  plt.plot(x_values, hump_shaped_list, label='Hump-Shaped')
  plt.plot(x_values, others_list, label='Other')
  plt.plot(x_values, x_values, label='Perfect CC')

  # Add labels and title
  plt.xlabel('Average Investment of Group Members')
  plt.ylabel('Your Investment (Investment Table)')
  plt.title('Conditional Investment Plot Partitioned by Player-Types')

  plt.xlim(0, 20)
  plt.ylim(0, 20)
  plt.xticks(range(0, 21))
  plt.yticks(range(0, 21)) 


  # Add legend
  plt.legend()

  # Show the plot
  plt.show()
