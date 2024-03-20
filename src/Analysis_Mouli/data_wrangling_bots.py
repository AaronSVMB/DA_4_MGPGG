# %%

# importing packages

import pandas as pd
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"

from scipy import stats

from datetime import datetime
import os

# importing own functions

from data_wrangling_functions import(maximum_col_group_by_own_investment,
                                     maximum_com_group_by_own_investment,
                                     maximum_col_group_by_other_last_investment,
                                     maximum_com_group_by_other_last_investment,
                                     minimum_col_group_by_own_investment,
                                     minimum_com_group_by_own_investment,
                                     minimum_col_group_by_other_last_investment,
                                     minimum_com_group_by_other_last_investment)

#%%

# Creating folder in output folder with date of execution to store all results

# Setting output directory
output_folder = r"C:\Users\modak\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"

# Different paths
## Mouli (Personal): r"C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"
## Mouli (Work): r"C:\Users\modak\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"

today = datetime.now()
path = output_folder+"\{}".format(today.strftime('%Y-%m-%d'))

if os.path.exists(path) == False:
    os.mkdir(path)

output_location = path

# Input Folder

input_folder = r"C:\Users\modak\Dropbox\Work\Projects\Multigroup PG\Analysis\Input"

# Different paths
## bots: Mouli (Personal): r"C:\Users\mouli\Dropbox\Multigroup PGG\Data\Fall 2023"
## bots: Mouli (Work): r"C:\Users\modak\Dropbox\Work\Multigroup PGG\Data\Fall 2023"
## Bots: Mouli (Personal): r"C:\Users\mouli\Dropbox\Work\Multigroup PGG\Data\Extension"
## Bots: Mouli (Work): r"C:\Users\modak\Dropbox\Work\Multigroup PGG\Data\Extension"

file_name = r"\mgpgg_extension_all_df.csv"

# Different file names
## Bots = \mgpgg_extension_all_df.csv
## bots = \mgpgg_df_all_sessions.csv

# %%

# Importing Data

bots_all_df = pd.read_csv(input_folder + file_name, low_memory=False)
# print(bots_all_df.head())

print("Column Names:")
for col in bots_all_df.columns:
    print(col)

# %%

# Columns to be renamed

old_colnames_tokeep = [
    "participant.code",
    "player.id_in_group",
    "player.payoff",
    "player.blue_group_human_partner",
    "player.green_group_human_partner",
    "player.blue_group_total_investment",
    "player.blue_group_individual_share",
    "player.green_group_total_investment",
    "player.green_group_individual_share",
    "player.blue_group_profit",
    "player.green_group_profit",
    "player.personal_account",
    "player.blue_group_investment",
    "player.green_group_investment",
    "player.blue_bot_one_investment",
    "player.blue_bot_two_investment",
    "player.green_bot_one_investment",
    "player.green_bot_two_investment",
    "group.id_in_subsession",
    "subsession.round_number",
    "session.code",
    "blue_green",
    "player.bot_number_blue",
    "player.bot_level_blue",
    "player.bots_pattern_blue",
    "player.bots_own_blue",
    "player.bots_understand_blue",
    "player.bot_number_green",
    "player.bot_level_green",
    "player.bots_pattern_green",
    "player.bots_own_green",
    "player.bots_understand_green",
    "bots",
    "player.better_group_investment",
    "player.worse_group_investment",
    "better_group",
    "worse_group",
    "player.better_group_total_investment",
    "player.worse_group_total_investment",
    "player.better_group_bot_investment",
    "player.worse_group_bot_investment",
]

renamed_colnames = [
    a.replace(".","_") for a in old_colnames_tokeep
]

# print(renamed_colnames)
# %%

# Generating experiment data

## Keeping necessary columns
bots_experiment_df = bots_all_df[old_colnames_tokeep]
bots_experiment_df = bots_experiment_df.rename(columns=dict(zip(old_colnames_tokeep, renamed_colnames)))
bots_experiment_df["Treatment"] = "Multi-Shared"
# print(bots_experiment_df.head())

## More and Less Own Contribution
bots_experiment_df["player_more_investment"] = bots_experiment_df[["player_blue_group_investment", "player_green_group_investment"]].max(axis=1)
bots_experiment_df["player_less_investment"] = bots_experiment_df[["player_blue_group_investment", "player_green_group_investment"]].min(axis=1)

print(bots_experiment_df["player_more_investment"])

## Others' contribution
bots_experiment_df["player_others_blue_group_investment"] = bots_experiment_df["player_blue_group_total_investment"] - bots_experiment_df["player_blue_group_investment"]
bots_experiment_df["player_others_green_group_investment"] = bots_experiment_df["player_green_group_total_investment"] - bots_experiment_df["player_green_group_investment"]
bots_experiment_df["player_others_better_group_investment"] = bots_experiment_df["player_better_group_total_investment"] - bots_experiment_df["player_better_group_investment"]
bots_experiment_df["player_others_worse_group_investment"] = bots_experiment_df["player_worse_group_total_investment"] - bots_experiment_df["player_worse_group_investment"]

bots_experiment_df["player_other_human_blue_group_investment"] = bots_experiment_df["player_others_blue_group_investment"] - bots_experiment_df["player_blue_bot_one_investment"] - bots_experiment_df["player_blue_bot_two_investment"]
bots_experiment_df["player_other_human_green_group_investment"] = bots_experiment_df["player_others_green_group_investment"] - bots_experiment_df["player_green_bot_one_investment"] - bots_experiment_df["player_green_bot_two_investment"]

bots_experiment_df["player_total_PGG_investment"] = bots_experiment_df["player_blue_group_investment"] + bots_experiment_df["player_green_group_investment"]

## Last Period Data
temp_df = bots_experiment_df[[
    "participant_code",
    "player_id_in_group",
    "player_blue_group_human_partner",
    "player_green_group_human_partner",
    "player_blue_group_total_investment",
    "player_blue_group_individual_share",
    "player_green_group_total_investment",
    "player_green_group_individual_share",
    "player_blue_group_profit",
    "player_green_group_profit",
    "player_personal_account",
    "player_blue_group_investment",
    "player_green_group_investment",
    "player_blue_bot_one_investment",
    "player_blue_bot_two_investment",
    "player_green_bot_one_investment",
    "player_green_bot_two_investment",
    "group_id_in_subsession",
    "subsession_round_number",
    "session_code",
    "player_better_group_investment",
    "player_worse_group_investment",
    "player_more_investment",
    "player_less_investment",
    "player_better_group_total_investment",
    "player_worse_group_total_investment",
    "player_better_group_bot_investment",
    "player_worse_group_bot_investment",
    "player_others_blue_group_investment",
    "player_others_green_group_investment",
    "player_others_better_group_investment",
    "player_others_worse_group_investment",
    "player_other_human_blue_group_investment",
    "player_other_human_green_group_investment",
    "player_total_PGG_investment",
]]

colnames_to_change = [
    "player_blue_group_human_partner",
    "player_green_group_human_partner",
    "player_blue_group_total_investment",
    "player_blue_group_individual_share",
    "player_green_group_total_investment",
    "player_green_group_individual_share",
    "player_blue_group_profit",
    "player_green_group_profit",
    "player_personal_account",
    "player_blue_group_investment",
    "player_green_group_investment",
    "player_blue_bot_one_investment",
    "player_blue_bot_two_investment",
    "player_green_bot_one_investment",
    "player_green_bot_two_investment",
    "player_better_group_investment",
    "player_worse_group_investment",
    "player_more_investment",
    "player_less_investment",
    "player_better_group_total_investment",
    "player_worse_group_total_investment",
    "player_better_group_bot_investment",
    "player_worse_group_bot_investment",
    "player_others_blue_group_investment",
    "player_others_green_group_investment",
    "player_others_better_group_investment",
    "player_others_worse_group_investment",
    "player_other_human_blue_group_investment",
    "player_other_human_green_group_investment",
    "player_total_PGG_investment",
]

colnames_last_period = [
    "L_player_blue_group_human_partner",
    "L_player_green_group_human_partner",
    "L_player_blue_group_total_investment",
    "L_player_blue_group_individual_share",
    "L_player_green_group_total_investment",
    "L_player_green_group_individual_share",
    "L_player_blue_group_profit",
    "L_player_green_group_profit",
    "L_player_personal_account",
    "L_player_blue_group_investment",
    "L_player_green_group_investment",
    "L_player_blue_bot_one_investment",
    "L_player_blue_bot_two_investment",
    "L_player_green_bot_one_investment",
    "L_player_green_bot_two_investment",
    "L_player_better_group_investment",
    "L_player_worse_group_investment",
    "L_player_more_investment",
    "L_player_less_investment",
    "L_player_better_group_total_investment",
    "L_player_worse_group_total_investment",
    "L_player_better_group_bot_investment",
    "L_player_worse_group_bot_investment",
    "L_player_others_blue_group_investment",
    "L_player_others_green_group_investment",
    "L_player_others_better_group_investment",
    "L_player_others_worse_group_investment",
    "L_player_other_human_blue_group_investment",
    "L_player_other_human_green_group_investment",
    "L_player_total_PGG_investment",
]

temp_df = temp_df.rename(columns=dict(zip(colnames_to_change, colnames_last_period)))

# print(temp_df.columns)

temp_df["subsession_round_number"] = temp_df["subsession_round_number"] + 1

L_bots_experiment_df = pd.merge(left=bots_experiment_df, right=temp_df, how="left", on=["participant_code", "player_id_in_group", "group_id_in_subsession", "subsession_round_number", "session_code"], validate="1:1")
# print(L_bots_experiment_df.columns)

# %%
    
## Creating new columns

L_bots_experiment_df["maximum_col_group_by_own_investment"] = L_bots_experiment_df.apply(lambda row : maximum_col_group_by_own_investment(row), axis=1) 
L_bots_experiment_df["minimum_col_group_by_own_investment"] = L_bots_experiment_df.apply(lambda row : minimum_col_group_by_own_investment(row), axis=1) 
L_bots_experiment_df["maximum_com_group_by_own_investment"] = L_bots_experiment_df.apply(lambda row : maximum_com_group_by_own_investment(row), axis=1) 
L_bots_experiment_df["minimum_com_group_by_own_investment"] = L_bots_experiment_df.apply(lambda row : minimum_com_group_by_own_investment(row), axis=1) 
L_bots_experiment_df["maximum_col_group_by_other_last_investment"] = L_bots_experiment_df.apply(lambda row : maximum_col_group_by_other_last_investment(row), axis=1) 
L_bots_experiment_df["minimum_col_group_by_other_last_investment"] = L_bots_experiment_df.apply(lambda row : minimum_col_group_by_other_last_investment(row), axis=1) 
L_bots_experiment_df["maximum_com_group_by_other_last_investment"] = L_bots_experiment_df.apply(lambda row : maximum_com_group_by_other_last_investment(row), axis=1) 
L_bots_experiment_df["minimum_com_group_by_other_last_investment"] = L_bots_experiment_df.apply(lambda row : minimum_com_group_by_other_last_investment(row), axis=1) 
# %%

L_bots_experiment_df.to_csv(input_folder+r"\bots_sessions_experiment_data.csv")

# %%
