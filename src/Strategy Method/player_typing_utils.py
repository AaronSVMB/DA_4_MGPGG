"""
For organizational purposes, this file handles all of the typings noted by fgf (2000) these include the classifications of; 
free-riders, conditional cooperators, hump-shaped (triange) contributors, and others (unclassifiable)
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================

from constants import np, pd, stats

# ====================================================================================================================
# Free-riders: anyone who gives 0 in all cases (for conditional investment)
# ====================================================================================================================


def find_freeriders(dataframe: np.ndarray, col_names: list):
  """
  From all players, this code determines which are freeriders by taking the sum
  of their contributions across all conditional investments; a free-rider has a
  sum of 0.

  :param dataframe - the strategy method dataframe that holds the Conditional investment information
  :param col_names - the name of the relevant columns; player.conditional_investment_0 ... _20
  :return: the updated dataframe with 2 additional columns: the sums and the 
  Truth value for each player being a FR
  """
  # sum conditional investment values
  dataframe['player.conditional_investment_sums'] = dataframe[col_names].sum(axis=1)
  # if == 0 free-rider; else non-free-rider
  dataframe['player.is_freerider'] = (dataframe['player.conditional_investment_sums'] == 0)
  return dataframe


# ====================================================================================================================
# Conditional Cooperator – all subjects who either show a monotonic pattern with at least one increase or have 
# a positive spearman rank correlation that is significant at the 1%-level
# ====================================================================================================================


def find_monotonic_and_increase(dataframe: np.ndarray, col_names: list):
  """
  This function is one of the two sufficient criteria for subjects who can be CCs; 
  monotonic pattern with at least one increase

  :param dataframe - the strategy method data that I continually add columns to
  :param col_names - the name of the relevant columns; player.conditional_investment_0 ... _20
  :return: the updated dataframe with an additional column with Truth values of
  whether subjects conditional investments showcase a monotonic and increase pattern
  """
  conditional_investment_players = dataframe.loc[:, col_names]
  # Check for Monotonicity and at least one Increase
  is_monotonic_list, has_one_increase_list = [], []
  for player in range(conditional_investment_players.shape[0]):
    player_decisions = conditional_investment_players.iloc[player]
    player_decisions_as_list = player_decisions.tolist()
    # check if trend satisfies monotonic
    is_monotonic = all(player_decisions_as_list[i] <= player_decisions_as_list[i+1] for i in range(len(player_decisions_as_list)-1))
    is_monotonic_list.append(is_monotonic)
    # check if at least one increase (not all the same)
    for i in range(len(player_decisions_as_list) - 1):
      if player_decisions_as_list[i+1] > player_decisions_as_list[i]:
        has_one_increase = True
        break
      else:
        has_one_increase = False
    has_one_increase_list.append(has_one_increase)
  
  is_monotonic_and_has_one_increase_list = [x and y for x, y in zip(is_monotonic_list, has_one_increase_list)]
  dataframe['player.is_monotonic_and_one_increase'] = is_monotonic_and_has_one_increase_list
  return dataframe


def find_pos_sig_spearman(dataframe: np.ndarray, col_names: list, x_values: list):
  """
  Second method to be classified as a CC; positive spearman rank correlation that
  is significnat at the 1% level

  :param dataframe - the strategy method data that I continually add columns to
  :param col_names - the name of the relevant columns; player.conditional_investment_0 ... _20
  :param x_values - values 0 ... 20 for average investment levels
  :return: updated dataframe with additional columns of direction of coefficient, 
  the p_value of the coefficient, and Truth value of whether it is pos and sig
  """
  conditional_investment_players = dataframe.loc[:, col_names]
  
  pos_sig_spearman_list, rho_list, p_value_list = [], [], []
  for player in range(conditional_investment_players.shape[0]):
    player_decisions = conditional_investment_players.iloc[player]
    player_decisions_as_list = player_decisions.tolist()
    rho, p_value = stats.spearmanr(x_values, player_decisions_as_list)
    if rho > 0 and p_value <= 0.01:
      pos_sig_spearman = True
    else:
      pos_sig_spearman = False
    rho_list.append(rho)
    p_value_list.append(p_value)
    pos_sig_spearman_list.append(pos_sig_spearman)

  dataframe['player.spearman_coeff'] = rho_list
  dataframe['player.spearman_p_value'] = p_value_list
  dataframe['player.positive_sig_spearman'] = pos_sig_spearman_list
  return dataframe
  

def find_conditional_cooperators(dataframe: np.ndarray):
  """
  Determine which players are CCs based on if they fit at least one of the CC criteria

  :param dataframe with necessary columns generated by 'find_pos_sig_spearman'
  and 'find_monotonic_and_increase' functions
  :return: the updated dataframe with an additional Truth columns corresponding
  to whether or not a subject behaves as a CC
  """
  dataframe['player.is_conditional_cooperator'] = dataframe['player.is_monotonic_and_one_increase'] | dataframe['player.positive_sig_spearman']
  return dataframe


# ====================================================================================================================
# Hump Shaped / Triangle Contributors – subjects who have a significant increase up to some maximum and a significant 
# decrease thereafter again using spearman rank test at the 1% level
# ====================================================================================================================


def find_hump_shaped(dataframe: np.ndarray, col_names: list, x_values: list):
  """
  FGF criteria for being hump shaped; method (1) find max value (2) compute
  spearman rank from start to max value (3) check if pos and sig (4) max to 
  end (5) check if neg and sig (6) if (3) and (5) correct sign and sig, then 
  the player if hump shaped; else not

  :param dataframe - the strategy method data that I continually add columns to
  :param col_names - the name of the relevant columns; player.conditional_investment_0 ... _20
  :param x_values - values 0 ... 20 for average investment levels
  :return: updated dataframe with additional Truth column for if a subject
  is hump shaped or not
  """
  conditional_investment_players = dataframe.loc[:, col_names]

  subset_pos_sig_spearman_list, subset_rho_list, subset_p_value_list  = [], [], []
  subset_neg_sig_spearman_list, subset_rho2_list, subset_p_value2_list = [], [], []

  for player in range(conditional_investment_players.shape[0]):
    player_decisions = conditional_investment_players.iloc[player]
    player_decisions_as_list = player_decisions.tolist()
    highest_value_index = player_decisions_as_list.index(max(player_decisions_as_list))
    # Start to Max Value
    rho, p_value = stats.spearmanr(x_values[:highest_value_index+1],player_decisions_as_list[:highest_value_index+1])
    if rho > 0 and p_value < 0.01:
      subset_pos_sig_spearman = True
    else:
      subset_pos_sig_spearman = False
    subset_rho_list.append(rho)
    subset_p_value_list.append(p_value)
    subset_pos_sig_spearman_list.append(subset_pos_sig_spearman)
    # Max Value to End
    rho2, p_value2 = stats.spearmanr(x_values[highest_value_index:],player_decisions_as_list[highest_value_index:])
    if rho2 < 0 and p_value <0.01:
      subset_neg_sig_spearman = True
    else:
      subset_neg_sig_spearman = False
    subset_rho2_list.append(rho2)
    subset_p_value2_list.append(p_value2)
    subset_neg_sig_spearman_list.append(subset_neg_sig_spearman)

  is_hump_shaped_list = [x and y for x, y in zip(subset_pos_sig_spearman_list, subset_neg_sig_spearman_list)]

  dataframe['player.is_hump_shaped'] = is_hump_shaped_list
  return dataframe


# ====================================================================================================================
# Other – All subjects who fail to be classified into the three above categories
# ====================================================================================================================


def find_others(dataframe: np.ndarray):
  """
  if player.is_freerider and player.is_conditional_cooperator and player.is_hump_shaped == False; then Other
  
  :param dataframe - the strategy method dataframe with the relevant columns (all other typings already done)
  :return: updated data frame with those classified as others
  """
  dataframe['player.is_other'] = ~(dataframe['player.is_freerider'] | dataframe['player.is_conditional_cooperator'] | dataframe['player.is_hump_shaped']) 
  return dataframe
  
# ====================================================================================================================
# All Typings – consolidates the above classifications into one function
# ====================================================================================================================


def fgf_typings(dataframe: np.ndarray, col_names: list, x_values: list):
  """
  Performs all the FGF typings in one function

  :param dataframe - the strategy method data that I continually add columns to
  :param col_names - the name of the relevant columns; player.conditional_investment_0 ... _20
  :param x_values - values 0 ... 20 for average investment levels
  :return: the updated dataframe with all typings conducted and Truth columns
  """
  # Free-riders
  dataframe = find_freeriders(dataframe, col_names)
  # CCs
  dataframe = find_monotonic_and_increase(dataframe, col_names)
  dataframe = find_pos_sig_spearman(dataframe, col_names, x_values)
  dataframe = find_conditional_cooperators(dataframe)
  # hump shaped / triangle
  dataframe = find_hump_shaped(dataframe, col_names, x_values)
  # Other
  dataframe = find_others(dataframe)
  return dataframe


def string_typings(row: int):
  """_summary_

  :param row: a row in the SM df
  :return: the string type of the player
  """
  if row['player.is_freerider']:
    return 'freerider'
  if row['player.is_conditional_cooperator'] and row['player.is_hump_shaped']:
    return 'hump' # FGF partition error in their defintiion, from inspection of investment table plots, we feel subjects more align with their hump typing | these can also be other's if we wish
  if row['player.is_conditional_cooperator']:
    return 'conditional'
  if row['player.is_hump_shaped']: 
    return 'hump'
  else:
    return 'other'
  
def type_column(dataframe: np.ndarray):
  """
  Add a new column with each value depending on certain conditions (their type)

  :param dataframe: the strategy method dataframe with all of the update columns regarding FGF player-typings
  :return: updated dataframe with a type column that is easily transfered to the Treatment DF
  """
  dataframe['player.typing'] = dataframe.apply(lambda row: string_typings(row), axis=1)
  return dataframe
