"""
Code from Hikari Hikari on stack overflow. Implementation of Fisher Exact test in python for > 2x2 contingency table
Shown to produce same result as stats in R. 
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import math, np, stats


# ====================================================================================================================
# Depth First Search
# ====================================================================================================================


def _dfs(mat, pos, r_sum, c_sum, p_0, p):

    (xx, yy) = pos
    (r, c) = (len(r_sum), len(c_sum))

    mat_new = []

    for i in range(len(mat)):
        temp = []
        for j in range(len(mat[0])):
            temp.append(mat[i][j])
        mat_new.append(temp)

    if xx == -1 and yy == -1:
        for i in range(r-1):
            temp = r_sum[i]
            for j in range(c-1):
                temp -= mat_new[i][j]
            mat_new[i][c-1] = temp
        for j in range(c-1):
            temp = c_sum[j]
            for i in range(r-1):
                temp -= mat_new[i][j]
            mat_new[r-1][j] = temp
        temp = r_sum[r-1]
        for j in range(c-1):
            temp -= mat_new[r-1][j]
        if temp <0:
            return
        mat_new[r-1][c-1] = temp

        p_1 = 1
        for x in r_sum:
            p_1 *= math.factorial(x)
        for y in c_sum:
            p_1 *= math.factorial(y)

        n = 0
        for x in r_sum:
            n += x
        p_1 /= math.factorial(n)

        for i in range(len(mat_new)):
            for j in range(len(mat_new[0])):
                p_1 /= math.factorial(mat_new[i][j])
        if p_1 <= p_0 + 0.00000001:
            #print(mat_new)
            #print(p_1)
            p[0] += p_1
    else:
        max_1 = r_sum[xx]
        max_2 = c_sum[yy]
        for j in range(c):
            max_1 -= mat_new[xx][j]
        for i in range(r):
            max_2 -= mat_new[i][yy]
        for k in range(min(max_1,max_2)+1):
            mat_new[xx][yy] = k
            if xx == r-2 and yy == c-2:
                pos_new = (-1, -1)
            elif xx == r-2:
                pos_new = (0, yy+1)
            else:
                pos_new = (xx+1, yy)
            _dfs(mat_new, pos_new, r_sum, c_sum, p_0, p)


# ====================================================================================================================
# Fisher Exact Test (Produces p-value)
# ====================================================================================================================


def fisher_exact(table):

    row_sum = []
    col_sum = []

    for i in range(len(table)):
        temp = 0
        for j in range(len(table[0])):
            temp += table[i][j]
        row_sum.append(temp)
    
    for j in range(len(table[0])):
        temp = 0
        for i in range(len(table)):
            temp += table[i][j]
        col_sum.append(temp)

    mat = [[0] * len(col_sum)] * len(row_sum)
    pos = (0, 0)

    p_0 = 1

    for x in row_sum:
        p_0 *= math.factorial(x)
    for y in col_sum:
        p_0 *= math.factorial(y)

    n = 0
    for x in row_sum:
        n += x
    p_0 /= math.factorial(n)

    for i in range(len(table)):
        for j in range(len(table[0])):
            p_0 /= math.factorial(table[i][j])

    p = [0]
    _dfs(mat, pos, row_sum, col_sum, p_0, p)

    return p[0]


# ====================================================================================================================
# Generate Contingency Tables
# ====================================================================================================================


def gen_contingency_table(player_type_each_session_list: list):
  """
  generate contingency table to be used in fisher exact test 

  :param player_type_each_session_list - list of dictionaries for the count of each player type in each session
  :return: numpy array that is the sessions X number of types in the following order (FR, CC, HS, OT) with each
  entry being the count that occured in that session 
  """
  contingency_table = np.empty((len(player_type_each_session_list), 4))  # sessions x num_player_types (4)
  for session in range(len(player_type_each_session_list)):
    session_free_riders = player_type_each_session_list[session]['num_free_rider']
    session_conditional_cooperators = player_type_each_session_list[session]['num_conditional_cooperators']
    session_hump_shaped = player_type_each_session_list[session]['num_hump_shaped']
    session_other = player_type_each_session_list[session]['num_other']
    pt_list = [session_free_riders, session_conditional_cooperators, session_hump_shaped, session_other]
    for player_type in range(len(pt_list)):
      contingency_table[session, player_type] = pt_list[player_type]
  contingency_table = contingency_table.astype(int)
  return contingency_table


# ====================================================================================================================
# Chi-2 Test
# ====================================================================================================================


def gen_chi_2(distribution_one: np.ndarray, distribution_two: np.ndarray):
  """
  generate the chi-2 test for two distributions (importantly our own and one of the 2 others)
  in fgq 2012, they use this as a robustness check and show that their SM findings are similar to FGF

  :param distribution_one - one of the counts in order (FR, CC, HS, OT)
  :param distribution_two - the second counts in order (FR, CC, HS, OT)
  :return: the chi-2 statistic, the p-value, the degrees of freedom, and the expected values in each cell
  """
  contingency_table = np.vstack((distribution_one, distribution_two))
  chi2, p, dof, ex = stats.chi2_contingency(contingency_table)
  return chi2, p, dof, ex


# ====================================================================================================================
# Organization
# ====================================================================================================================


def gen_stat_test_dict(fisher_p_val: float, 
                       fgf_chi2: float, fgf_p_val: float, fgf_dof: int, fgf_ex: list,
                       fgq_chi2: float, fgq_p_val: float, fgq_dof: int, fgq_ex: list):
    stat_test_dict = {
        'fisher_p_val': fisher_p_val,
        'fgf_chi2': fgf_chi2,
        'fgf_p_val': fgf_p_val,
        'fgf_dof': fgf_dof,
        'fgf_ex': fgf_ex,
        'fgq_chi2': fgq_chi2,
        'fgq_p_val': fgq_p_val,
        'fgq_dof': fgq_dof,
        'fgq_ex': fgq_ex
    }
    return stat_test_dict