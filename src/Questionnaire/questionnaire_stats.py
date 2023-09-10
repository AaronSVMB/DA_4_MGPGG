"""
Some statistics from the all_questionnaire_df
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd


# ====================================================================================================================
# Gender, Age, Grade, Major, Risk
# ====================================================================================================================


def gen_gender_dict(all_questionnaire_df: pd.DataFrame):
    """
    Gender breakdown

    :param all_questionnaire_df: conbined DF from our 3 survey types
    :return gender_dict: information regarding gender
    """
    # Count the occurrences of each unique value in the 'Fruit' column
    count_gender_series = all_questionnaire_df['player.gender'].value_counts()

    # Convert the Series to a dictionary
    gender_dict = count_gender_series.to_dict()

    gender_dict['female'] =  gender_dict.pop(2.0)
    gender_dict['male'] =  gender_dict.pop(1.0)
    gender_dict['other'] =  gender_dict.pop(3.0)

    return gender_dict

def gen_age_dict(all_questionnaire_df: pd.DataFrame):
    """
    Age breakdown

    :param all_questionnaire_df: conbined DF from our 3 survey types
    """
    count_age_series = all_questionnaire_df['player.age'].value_counts()

    age_dict = count_age_series.to_dict()

    return age_dict

def gen_grade_dict(all_questionnaire_df: pd.DataFrame):
    """
    Grade breakdown

    :param all_questionnaire_df: conbined DF from our 3 survey types
    """
    count_grade_series = all_questionnaire_df['player.grade'].value_counts()

    grade_dict = count_grade_series.to_dict()

    grade_dict['freshman'] =  grade_dict.pop(1.0)
    grade_dict['sophomore'] =  grade_dict.pop(2.0)
    grade_dict['junior'] =  grade_dict.pop(3.0)
    grade_dict['senior'] =  grade_dict.pop(4.0)
    grade_dict['graduate'] =  grade_dict.pop(5.0)

    return grade_dict

def gen_major_dict(all_questionnaire_df: pd.DataFrame):
    """
    Major breakdown

    :param all_questionnaire_df: conbined DF from our 3 survey types
    """
    count_major_series = all_questionnaire_df['player.major'].value_counts()

    major_dict = count_major_series.to_dict()

    return major_dict

def gen_risk_dict(all_questionnaire_df: pd.DataFrame):
    """
    Risk scale breakdown

    :param all_questionnaire_df: conbined DF from our 3 survey types
    """
    count_risk_series = all_questionnaire_df['player.risk'].value_counts()

    risk_dict = count_risk_series.to_dict()

    risk_dict_structure = {1.0: 0,
                           2.0: 0,
                           3.0: 0,
                           4.0: 0,
                           5.0: 0,
                           6.0: 0,
                           7.0: 0}

    risk_dict_final = {key: risk_dict.get(key, 0) + risk_dict_structure.get(key, 0) for key in set(risk_dict) | set(risk_dict_structure)}

    risk_dict_final['strongly disagree'] = risk_dict_final.pop(1.0)
    risk_dict_final['disagree'] = risk_dict_final.pop(2.0)
    risk_dict_final['slightly disagree'] = risk_dict_final.pop(3.0)
    risk_dict_final['neutral'] = risk_dict_final.pop(4.0)
    risk_dict_final['slightly agree'] = risk_dict_final.pop(5.0)
    risk_dict_final['agree'] = risk_dict_final.pop(6.0)
    risk_dict_final['strongly agree'] = risk_dict_final.pop(7.0)

    return risk_dict_final


# ====================================================================================================================
# Scale Questions (Larry MG and Larry Single)
# ====================================================================================================================

def gen_motivation_dict(all_questionnaire_df: pd.DataFrame, column_name: str):
    """
    The breakdowns for all questions regarding the format of what motivated your response, since they use the same scaling,
    can be generated with this function

    :param all_questionnaire_df: conbined DF from our 3 survey types
    :return: dict breakdown of the reason why x investment from subjects on a scale
    """
    count_motivation_series = all_questionnaire_df[column_name].value_counts()

    moviation_dict = count_motivation_series.to_dict()

    motivation_structure = {1.0: 0,
                           2.0: 0,
                           3.0: 0,
                           4.0: 0,
                           5.0: 0
                           }

    motivation_dict_final = {key: moviation_dict.get(key, 0) + motivation_structure.get(key, 0) for key in set(moviation_dict) | set(motivation_structure)}

    motivation_dict_final['strongly agree'] = motivation_dict_final.pop(1.0)
    motivation_dict_final['agree'] = motivation_dict_final.pop(2.0)
    motivation_dict_final['disagree'] = motivation_dict_final.pop(3.0)
    motivation_dict_final['strongly disagree'] = motivation_dict_final.pop(4.0)
    motivation_dict_final['uncertain'] = motivation_dict_final.pop(5.0)

    return motivation_dict_final




# ====================================================================================================================
# Decision Style
# ====================================================================================================================

#TODO 
# Will need 2 separate functions | one for Aaron's survey (5 levels) and one for Larry's survey (4 levels) 
# And Larry's survey has additional questions of this variety


# ====================================================================================================================
# Clarity
# ====================================================================================================================

def gen_clarity_dict(all_questionnaire_df: pd.DataFrame):
    """
    Instruction clarity scores

    :param all_questionnaire_df: conbined DF from our 3 survey types
    """
    count_clarity_series = all_questionnaire_df['player.clarity'].value_counts()

    clarity_dict = count_clarity_series.to_dict()

    clarity_dict_structure = {1.0: 0,
                           2.0: 0,
                           3.0: 0,
                           4.0: 0,
                           5.0: 0,
                           }

    clarity_dict_final = {key: clarity_dict.get(key, 0) + clarity_dict_structure.get(key, 0) for key in set(clarity_dict) | set(clarity_dict_structure)}

    clarity_dict_final['strongly disagree'] = clarity_dict_final.pop(1.0)
    clarity_dict_final['disagree'] = clarity_dict_final.pop(2.0)
    clarity_dict_final['agree'] = clarity_dict_final.pop(3.0)
    clarity_dict_final['strongly agree'] = clarity_dict_final.pop(4.0)
    clarity_dict_final['dont know'] = clarity_dict_final.pop(5.0)

    return clarity_dict_final
