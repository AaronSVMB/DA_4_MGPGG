import pandas as pd

## Row functions used to modify dataframe

def maximum_col_group_by_own_investment(row):

    if row.blue_investment > row.green_investment:
        return "Blue"
    elif row.blue_investment < row.green_investment:
        return "Green"
    else:
        return "Equal"

def minimum_col_group_by_own_investment(row):
    if row.maximum_col_group_by_own_investment == "Blue":
        return "Green"
    elif row.maximum_col_group_by_own_investment == "Green":
        return "Blue"
    else:
        return "Equal"

def maximum_col_group_by_other_last_investment(row):
    if row.L_others_blue_investment > row.L_others_green_investment:
        return "Blue"
    elif row.L_others_blue_investment < row.L_others_green_investment:
        return "Green"
    else:
        return "Equal"

def minimum_col_group_by_other_last_investment(row):
    if row.maximum_col_group_by_other_last_investment == "Blue":
        return "Green"
    elif row.maximum_col_group_by_other_last_investment == "Green":
        return "Blue"
    else:
        return "Equal"

def maximum_com_group_by_own_investment(row):

    if row.better_group_investment > row.worse_group_investment:
        return "Better"
    elif row.better_group_investment < row.worse_group_investment:
        return "Worse"
    else:
        return "Equal"

def minimum_com_group_by_own_investment(row):
    if row.maximum_com_group_by_own_investment == "Better":
        return "Worse"
    elif row.maximum_com_group_by_own_investment == "Worse":
        return "Better"
    else:
        return "Equal"

def maximum_com_group_by_other_last_investment(row):
    if row.L_others_better_group_investment > row.L_others_worse_group_investment:
        return "Better"
    elif row.L_others_better_group_investment < row.L_others_worse_group_investment:
        return "Worse"
    else:
        return "Equal"

def minimum_com_group_by_other_last_investment(row):
    if row.maximum_com_group_by_other_last_investment == "Better":
        return "Worse"
    elif row.maximum_com_group_by_other_last_investment == "Worse":
        return "Better"
    else:
        return "Equal"

def player_total_payoff(row):

    if row["treatment"] == "Single Group":
        ret = row["personal_account"] + row["individual_share"]
    else:
        ret = row["personal_account"] + row["blue_individual_share"] + row["green_individual_share"]
    # print(ret)
    return ret

def total_pg_investment(row):

    if row["treatment"] == "Single Group":
        ret = row["investment"]
    else:
        ret = row["blue_investment"] + row["green_investment"]

    return ret

def rename_treatments(row):
    if row.treatment == "Multi-Shared":
        return "Multi-Shared (Humans)"
    elif row.treatment == "Bots Unbalanced":
        return "Multi-Shared (Bots Unbalanced)"
    elif row.treatment == "Bots Balanced":
        return "Multi-Shared (Bots Balanced)"
    else:
        return row.treatment

def rename_accounts(row):

    if row['Account'] == 0:
        ret = "Total"
    elif row['Account'] == 1:
        ret = "Personal"
    elif row['Account'] == 2:
        ret = "Blue"
    elif row['Account'] == 3:
        ret = "Green"

    return ret

def grouping_diff_others_investment(row):

    if (row["L_diff_others_group_investment"] >= -20) & (row["L_diff_others_group_investment"] < -15):
        return 1
    elif (row["L_diff_others_group_investment"] >= -15) & (row["L_diff_others_group_investment"] < -10):
        return 2
    elif (row["L_diff_others_group_investment"] >= -10) & (row["L_diff_others_group_investment"] < -5):
        return 3
    elif (row["L_diff_others_group_investment"] >= -5) & (row["L_diff_others_group_investment"] < 0):
        return 4
    elif row["L_diff_others_group_investment"] == 0:
        return 5
    elif (row["L_diff_others_group_investment"] > 0) & (row["L_diff_others_group_investment"] <= 5):
        return 6
    elif (row["L_diff_others_group_investment"] > 5) & (row["L_diff_others_group_investment"] <= 10):
        return 7
    elif (row["L_diff_others_group_investment"] > 10) & (row["L_diff_others_group_investment"] <= 15):
        return 8
    elif (row["L_diff_others_group_investment"] > 15) & (row["L_diff_others_group_investment"] <= 20):
        return 9    