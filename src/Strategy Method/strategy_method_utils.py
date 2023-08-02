"""
Code for data analysis of the Strategy Method data
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from sm_data_clean_utils import sm_reading_and_cleaning
from player_typing_utils import fgf_typings, type_column
from counting_utils import gen_player_type_distributions, gen_ibm_distribution
# Can reduce in future (only need the last two)
from stat_tests_utils import fisher_exact, gen_contingency_table, gen_chi_2, gen_stat_test_dict
from constants import (conditional_investment_list, conditional_investment_x_values, 
                       fgf_distribution, fgq_distrubtion, np)
from investment_utils import gen_unconditional_investment_avgs, gen_avg_conditional_investments, fgf_plot


# ====================================================================================================================
# Run it all together
# ====================================================================================================================

def strategy_method_analysis(filename: str, x_values: list, col_names: list,
                              fgf_distribution: np.ndarray, fgq_distribution: np.ndarray, num_sessions: int):
    """Conducts all of the imported data analysis functionalities in one fell swoop

    :param filename: the oTree data for the strategy method
    :param x_values: the values 0, 1, 2, 3, ... 20 for the group conditional investment avgs
    :param col_names: the column names where subjects conditional decisions are stored
    :param distribution_one: fgf distribution
    :param distribution_two: fgq distribution
    :param num_sessions: the number of sessions that are in the data set
    :return: (1)the updated df with all cleaned columns and added info, (2) the player types across all session dict,
    the (3) player types within in each session distribution, (4) stat test dict, 
    (5) avg unconditional info, (6) avg conditional info.
    """
    # read and clean the data set
    smdf = sm_reading_and_cleaning(filename)
    # add columns that type players
    smdf = fgf_typings(smdf, col_names, x_values)
    # find the distribution (1) across all sessions (2) for each session
    all_sessions_player_type_dict, player_types_per_session_list = gen_player_type_distributions(smdf)
    # string player type columns for ease of transferability to another dataframe (Treatment DF)
    smdf = type_column(smdf)

    # Use Fisher Exact test to check the distribution of preference types is the same across all sessions
    if num_sessions != 1:
        player_type_cont_table = gen_contingency_table(player_types_per_session_list)
        fisher_p_value = fisher_exact(player_type_cont_table)
    else:
        fisher_p_value = float('-inf')
    # Chi-2 test as a robustness check with FGF and FGQ data; goal is to not reject the null of equal dist with
    # our sample compared to their sample: order (FR, CC, HS, OT)
    ibm_distribution = gen_ibm_distribution(all_sessions_player_type_dict)
    # IBM versus FGF
    ibm_fgf_chi2, ibm_fgf_p, ibm_fgf_dof, ibm_fgf_ex = gen_chi_2(ibm_distribution, fgf_distribution)
    # IBM versus FGQ
    ibm_fgq_chi2, ibm_fgq_p, ibm_fgq_dof, ibm_fgq_ex = gen_chi_2(ibm_distribution, fgq_distribution)
    # Store stat tests as dictionary
    stat_test_dict = gen_stat_test_dict(fisher_p_value, ibm_fgf_chi2, ibm_fgf_p, ibm_fgf_dof, ibm_fgf_ex,
                                        ibm_fgq_chi2, ibm_fgq_p, ibm_fgq_dof, ibm_fgq_ex)
    # Unconditional Investment Averages
    unconditional_dict = gen_unconditional_investment_avgs(smdf)
    # Conditional Investment
    conditional_dict = gen_avg_conditional_investments(smdf, col_names)
    # Plot the conditional
    fgf_plot(x_values, conditional_dict)
    # Save DF as csv
    smdf.to_csv('Analyzed_SM_Data.csv', index=False)
    return smdf, all_sessions_player_type_dict, player_types_per_session_list, stat_test_dict, unconditional_dict, conditional_dict



