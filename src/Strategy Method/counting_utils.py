"""
Count the occurance of the various player types in each session, among all the sessions, etc.
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import np


# ====================================================================================================================
# Count Player Types – All Sessions
# ====================================================================================================================


def gen_players_and_types_dict(dataframe: np.ndarray):
  """
  Constructs dictionary to establish distribution of player types across all sessions

  :param dataframe - strategy method dataframe with all player typing conducted
  :return: dictionary with player type keys and counts of each as values
  """
  num_players = dataframe.shape[0]
  num_free_riders = (dataframe['player.is_freerider'] == True).sum()
  num_conditonal_cooperators = (dataframe['player.is_conditional_cooperator'] == True).sum()
  num_hump_shaped = (dataframe['player.is_hump_shaped'] == True).sum()
  num_other = (dataframe['player.is_other'] == True).sum()

  player_type_count_dict = {'num_players':num_players, 'num_free_rider':num_free_riders,
                          'num_conditional_cooperators': num_conditonal_cooperators, 'num_hump_shaped': num_hump_shaped,
                          'num_other': num_other}
  return player_type_count_dict


# ====================================================================================================================
# Count Player Types – For Each Session
# ====================================================================================================================


def find_session_ids(dataframe: np.ndarray):
  """
  generates a list of the unique session ids (oTree produces one for each session)

  :param dataframe - strategy method dataframe with all player typing conducted
  :return: list of length # of sessions with each entry being oTree's genereated session code
  """
  session_ids = dataframe['session.code'].unique().tolist()
  return session_ids


def gen_player_type_each_session(dataframe: np.ndarray, session_id_list: list):
  """
  create a list of dictionaries to have a breakdown of distribution within each
  session

  :param dataframe - strategy method dataframe with all player typing conducted
  :param session_id_list - list of unique session codes 
  :return: list of dictionaries for each sessions player type distributions
  """
  player_types_per_session_list = []
  for index, session_id in enumerate(session_id_list):
    session_subset = dataframe[dataframe['session.code'] == session_id]
    session_player_type_dict = gen_players_and_types_dict(session_subset)
    player_types_per_session_list.append(session_player_type_dict)
  return player_types_per_session_list
    

# ====================================================================================================================
# Count Player Types – For Both Once
# ====================================================================================================================


def gen_player_type_distributions(dataframe: np.ndarray):
  """
  For ease of access later, perform all counting and distribution functions within one function
  
  :param dataframe - strategy method dataframe with all player typing conducted
  :return: two dictionaries (1) all sesions player typings (2) list of dicts for each session
  """
  all_sessions_player_type_dict = gen_players_and_types_dict(dataframe)
  session_id_list = find_session_ids(dataframe)
  player_types_per_session_list = gen_player_type_each_session(dataframe, session_id_list)
  return all_sessions_player_type_dict, player_types_per_session_list


# ====================================================================================================================
# Our Player type distributions
# ====================================================================================================================


def gen_ibm_distribution(player_type_count_dict: dict):
  """
  generate the ibm distribution (Iannaccone, Berman, and Modak 2023) of our player types

  :param player_type_count_dict - for all of our sessions the counts of each player type
  :return: returns the count for our players as a np.ndarray (FR, CC, HS, OT)
  """
  ibm_distribution = np.empty((1, 4))  # sessions x num_player_types (4)
  free_rider_count = player_type_count_dict['num_free_rider']
  conditional_coop_count = player_type_count_dict['num_conditional_cooperators']
  hump_shaped_count = player_type_count_dict['num_hump_shaped']
  other_count = player_type_count_dict['num_other']
  pt_list = [free_rider_count, conditional_coop_count, hump_shaped_count, other_count]
  for player_type in range(len(pt_list)):
    ibm_distribution[0, player_type] = pt_list[player_type]
  ibm_distribution = ibm_distribution.astype(int)
  return ibm_distribution