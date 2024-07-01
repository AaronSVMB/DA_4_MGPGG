# %%

# importing packages

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

from datetime import datetime
import os

# importing own functions

from data_wrangling_functions import(maximum_col_group_by_own_investment,
                                     maximum_col_group_by_other_last_investment,
                                     minimum_col_group_by_own_investment,
                                     minimum_col_group_by_other_last_investment,
                                     player_total_payoff,
                                     total_pg_investment,rename_treatments)
#%%

# Creating folder in output folder with date of execution to store all results

# Setting output directory
output_folder = r"C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"

# Different paths
## Mouli (Personal): r"C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"
## Mouli (Work): r"C:\Users\modak\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"

today = datetime.now()
path = output_folder+"\{}".format(today.strftime('%Y-%m-%d'))

if os.path.exists(path) == False:
    os.mkdir(path)

output_location = path

# Input Folder

input_folder = r"C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Input"
input_folder_custom = r"C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Input"

file_name = r"\mgpgg_all_data_df.csv"

# Different file names
## main = \mgpgg_extension_all_df.csv
## Main = \mgpgg_df_all_sessions.csv

# %%

# Importing Data

all_data_df = pd.read_csv(input_folder + file_name, low_memory=False)

print("Column Names:")
for col in all_data_df.columns:
    print(col)
# %%

# Column renaming

old_colnames_tokeep = [
    "pgg_treatment_applied",
    "participant.code",
    "player.id_in_group",
    "player.investment",
    "player.personal_account",
    "player.indiv_share",
    "player.tot_invest",
    "player.blue_group_partner_one_id",
    "player.blue_group_partner_two_id",
    "player.blue_group_partner_three_id",
    "player.blue_group_total_investment",
    "player.blue_group_individual_share",
    "player.green_group_partner_one_id",
    "player.green_group_partner_two_id",
    "player.green_group_partner_three_id",
    "player.green_group_total_investment",
    "player.green_group_individual_share",
    "player.blue_group_profit",
    "player.green_group_profit",
    "player.blue_group_investment",
    "player.green_group_investment",
    "group.id_in_subsession",
    "group.total_investment",
    "group.individual_share",
    "subsession.round_number",
    "session.code",
    "player.unconditional_investment",
    "player.conditional_investment_0",
    "player.conditional_investment_1",
    "player.conditional_investment_2",
    "player.conditional_investment_3",
    "player.conditional_investment_4",
    "player.conditional_investment_5",
    "player.conditional_investment_6",
    "player.conditional_investment_7",
    "player.conditional_investment_8",
    "player.conditional_investment_9",
    "player.conditional_investment_10",
    "player.conditional_investment_11",
    "player.conditional_investment_12",
    "player.conditional_investment_13",
    "player.conditional_investment_14",
    "player.conditional_investment_15",
    "player.conditional_investment_16",
    "player.conditional_investment_17",
    "player.conditional_investment_18",
    "player.conditional_investment_19",
    "player.conditional_investment_20",
    "player.am_i_the_conditional_investor",
    "player.time_spent_unconditional",
    "player.time_spent_conditional",
    "player.is_freerider",
    "player.is_monotonic_and_one_increase",
    "player.spearman_coeff",
    "player.spearman_p_value",
    "player.positive_sig_spearman",
    "player.is_conditional_cooperator",
    "player.is_hump_shaped",
    "player.is_other",
    "player.typing",
]

renamed_colnames = [
    a.replace(".","_") for a in old_colnames_tokeep
]

# %%

# Generating experiment data

## Keeping necessary columns

main_experiment_df = all_data_df.drop(labels=["Unnamed: 0", "demo"], axis=1)
print(main_experiment_df.head(5))

# main_experiment_df = main_experiment_df.rename(columns=dict(zip(old_colnames_tokeep, renamed_colnames)))
# main_experiment_df = main_experiment_df.rename(columns={"pgg_treatment_applied": "Treatment"})

# for col in main_experiment_df.columns:
#     print(col)

# %%

# Adding new columns

main_experiment_df["others_blue_investment"] = main_experiment_df["blue_total_invest"] - main_experiment_df["blue_investment"]
main_experiment_df["others_green_investment"] = main_experiment_df["green_total_invest"] - main_experiment_df["green_investment"]
main_experiment_df["others_investment"] = (main_experiment_df["total_investment"] - main_experiment_df["investment"])/3
main_experiment_df["total_payoff"] = main_experiment_df.apply(lambda row : player_total_payoff(row), axis=1) 
main_experiment_df["total_PGG_investment"] = main_experiment_df.apply(lambda row : total_pg_investment(row), axis=1)
main_experiment_df["treatment"] = main_experiment_df.apply(lambda row : rename_treatments(row), axis=1)

#%%

## More and Less Own Contribution
main_experiment_df["player_more_investment"] = main_experiment_df[["blue_investment", "green_investment"]].max(axis=1)
main_experiment_df["player_less_investment"] = main_experiment_df[["blue_investment", "green_investment"]].min(axis=1)

print(main_experiment_df["player_more_investment"])

#%%

# Last period data

temp_df = main_experiment_df[[
    "treatment",
    "session_code",
    "participant_code",
    "period",
    "participant_id",
    "investment",
    "personal_account",
    "individual_share",
    "total_investment",
    "blue_one_id",
    "blue_two_id",
    "blue_three_id",
    "blue_total_invest",
    "blue_individual_share",
    "green_one_id",
    "green_two_id",
    "green_three_id",
    "green_total_invest",
    "green_individual_share",
    "blue_period_profit",
    "green_period_profit",
    "blue_investment",
    "green_investment",
    "player_more_investment",
    "player_less_investment",
    "others_blue_investment",
    "others_green_investment",
    "others_investment",
    "total_payoff",
    "total_PGG_investment",
    # "total_PGG_investment",
    "group_id",
    "group_total_investment",
    "group_individual_share"
]]

colnames_to_change = [
    "investment",
    "personal_account",
    "individual_share",
    "total_investment",
    "blue_one_id",
    "blue_two_id",
    "blue_three_id",
    "blue_total_invest",
    "blue_individual_share",
    "green_one_id",
    "green_two_id",
    "green_three_id",
    "green_total_invest",
    "green_individual_share",
    "blue_profit",
    "green_profit",
    "personal_account",
    "blue_investment",
    "green_investment",
    "player_more_investment",
    "player_less_investment",
    "others_blue_investment",
    "others_green_investment",
    "others_investment",
    "total_payoff",
    "total_PGG_investment",
    "group_total_investment",
    "group_individual_share",
]

colnames_last_period = ["L_"+i for i in colnames_to_change]

temp_df = temp_df.rename(columns=dict(zip(colnames_to_change, colnames_last_period)))

# print(temp_df.columns)

temp_df["period"] = temp_df["period"] + 1

L_main_experiment_df = pd.merge(left=main_experiment_df, right=temp_df, how="left", on=["treatment","session_code", "participant_code", "period", "participant_id", "group_id"], validate="1:1")
# print(L_main_experiment_df.columns)

# %%
    
# Creating new columns

L_main_experiment_df["maximum_col_group_by_own_investment"] = L_main_experiment_df.apply(lambda row : maximum_col_group_by_own_investment(row), axis=1) 
L_main_experiment_df["minimum_col_group_by_own_investment"] = L_main_experiment_df.apply(lambda row : minimum_col_group_by_own_investment(row), axis=1) 
L_main_experiment_df["maximum_col_group_by_other_last_investment"] = L_main_experiment_df.apply(lambda row : maximum_col_group_by_other_last_investment(row), axis=1) 
L_main_experiment_df["minimum_col_group_by_other_last_investment"] = L_main_experiment_df.apply(lambda row : minimum_col_group_by_other_last_investment(row), axis=1) 

# %%

# print(L_main_experiment_df[(L_main_experiment_df.Treatment  != "Single Group") & (L_main_experiment_df.period != 1)][["period", "session_code", "Treatment", "L_player_others_blue_group_investment", "L_player_others_green_group_investment"]].head(10))

# %%

# Storing data

L_main_experiment_df.to_csv(input_folder_custom+r"\all_sessions_experiment_data.csv")

# %%
