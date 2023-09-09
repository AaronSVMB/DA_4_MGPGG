"""
Runs Risk Preference functionalities in one function. Speeds up future analysis as we have more data coming in
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================


from rp_data_clean_utils import rp_reading_and_cleaning
from rp_utils import count_num_safe, risk_estimation_bounds, assign_risk_preference_classifications


# ====================================================================================================================
# Time-saving, all in one-click function
# ====================================================================================================================

def gen_rp_one_click(filename: str, risk_estimation_lower_dict: dict, 
                 risk_estimation_upper_dict: dict, risk_classifications_dict: dict):
    """
    Performs Risk preference functionalities in one step

    :param filename: Risk Preference data set across all sessions to date
    :param risk_estimation_lower_dict: lower bound of r estimation
    :param risk_estimation_upper_dict: upper bound of r estimation
    :param risk_classifications_dict: Holt Laury names for each classification
    """
    df = rp_reading_and_cleaning(filename)
    count_num_safe(df)
    risk_estimation_bounds(df, risk_estimation_lower_dict, risk_estimation_upper_dict)
    assign_risk_preference_classifications(df, risk_classifications_dict)
    return df

