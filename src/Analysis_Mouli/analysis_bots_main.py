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

import pretty_errors

# importing own functions

from plot_functions import(plot_count_data, 
                           plot_avg_amount_account_byPeriod, 
                           plot_diff_BlueGreen, 
                           plot_avg_inv_diffaccount_byPeriod,
                           plot_order_effect)

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

file_name_main = r"\main_sessions_experiment_data.csv"
file_name_bots = r"\bots_sessions_experiment_data.csv"
file_name_custom = r"\all_sessions_treatment_strategy.csv"

# %%

# Importing Data


#* Uncomment this block or the next block, not both *#


## Block 1 -- Start ##
main_df = pd.read_csv(input_folder + file_name_main, low_memory=False)
main_df["Sessions"] = "Main"
bots_df = pd.read_csv(input_folder + file_name_bots, low_memory=False)
bots_df["Sessions"] = "Bots"
bots_df["Treatment"] = "Multi-Shared Bots"

all_sessions_df = pd.concat([main_df, bots_df], ignore_index=True)

all_sessions_df.to_csv(input_folder+r"\all_sessions_treatment_strategy.csv")
## Block 1 -- End ##

## Block 2 -- Start ##
# all_sessions_df = pd.read_csv(input_folder + r"\all_sessions_treatment_strategy.csv", low_memory=False, index_col=0)
## Block 2 -- End ##


print(all_sessions_df[(all_sessions_df.Treatment  != "Single Group") & (all_sessions_df.subsession_round_number != 1)][["subsession_round_number", "session_code", "Treatment", "L_player_others_blue_group_investment", "L_player_others_green_group_investment"]].head(10))

print("Column Names:")
for col in all_sessions_df.columns:
    print(col)

# %%

# Barplots (All Period)

# for account in ["Total"]:
#     for periods in ["AP"]:
#         plot_count_data(all_sessions_df, periods, account, "both", output_location)
        
#%%

# Line Plots (All Periods, By Periods)
        
plot_order_effect(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots")], output_location)

# for account in ["Total", "Blue", "Green", "Personal"]:
#     plot_avg_amount_account_byPeriod(all_sessions_df, account, "both", output_location)

# figure_details = {}

# figure_details["Type 1"] = {
#     "columns": ["player_more_investment", "player_less_investment"],
#     "labels": ["High Investment", "Low Investment"],
#     "colors": ["k", "r"],
#     "linestyle": ["-", "--"],
#     "name": "MaxMin",
# }

# figure_details["Type 2"] = {
#     "columns": ["player_blue_group_investment", "player_green_group_investment"],
#     "labels": ["Blue Account", "Green Account"],
#     "colors": ["b", "g"],
#     "linestyle": ["-", "--"],
#     "name": "BlueGreen",
# }

# figure_details["Type 3"] = {
#     "columns": ["player_more_investment", "player_less_investment", "player_blue_group_investment", "player_green_group_investment"],
#     "labels": ["High Investment", "Low Investment", "Blue Account", "Green Account"],
#     "colors": ["k", "r", "b", "g"],
#     "linestyle": ["-", "--", "-.", ":"],
#     "name": "MaxMin_BlueGreen",
# }

# figure_details["Type 4"] = {
#     "columns": ["player_better_group_investment", "player_worse_group_investment", "player_blue_group_investment", "player_green_group_investment"],
#     "labels": ["More Cooperative", "Less Cooperative", "Blue Account", "Green Account"],
#     "colors": ["k", "r", "b", "g"],
#     "linestyle": ["-", "--", "-.", ":"],
#     "name": "BW_BlueGreen",
# }

# figure_details["Type 5"] = {
#     "columns": ["player_better_group_investment", "player_worse_group_investment", "player_more_investment", "player_less_investment"],
#     "labels": ["More Cooperative", "Less Cooperative", "High Investment", "Low Investment"],
#     "colors": ["k", "r", "b", "g"],
#     "linestyle": ["-", "--", "-.", ":"],
#     "name": "MaxMin_BW",
# }


# for type in ["Type 1", "Type 2", "Type 3", "Type 4", "Type 5"]:

#     plot_avg_inv_diffaccount_byPeriod(all_sessions_df, figure_details[type]["columns"], figure_details[type]["colors"], figure_details[type]["linestyle"], figure_details[type]["labels"], figure_details[type]["name"], output_location)

    
#%%

# Difference between Blue and Green Groups

# plot_diff_BlueGreen(all_sessions_df, output_location)

# %%

# Comparing distributions

print("First Period")
  
stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)]["player_total_PGG_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots") & (all_sessions_df.subsession_round_number == 1)]["player_total_PGG_investment"])

print("Total PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))

stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)]["player_blue_group_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots") & (all_sessions_df.subsession_round_number == 1)]["player_blue_group_investment"])

print("Blue PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))

stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)]["player_green_group_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots") & (all_sessions_df.subsession_round_number == 1)]["player_green_group_investment"])

print("Blue PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))

print("All Periods")
  
stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared")]["player_total_PGG_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots")]["player_total_PGG_investment"])

print("Total PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))

stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared")]["player_blue_group_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots")]["player_blue_group_investment"])

print("Blue PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))

stat, pval = stats.kruskal(all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared")]["player_green_group_investment"], 
               all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared Bots")]["player_green_group_investment"])

print("Blue PGG Investment: stat = {}, pval = {}".format(round(stat, 3), round(pval, 3)))
# %%

# Swarm Plots

# plt.figure(figsize=(6,6))
# sns.swarmplot(data=all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)], x="Sessions", y="player_total_PGG_investment", color="k")
# plt.ylabel("Total Public Good Investment", fontsize = 16)
# plt.ylim(-1,21)
# plt.yticks(ticks=[0,2,4,6,8,10,12,14,16,18,20])
# plt.xlabel("Sessions", fontsize = 16)
# plt.xticks(fontsize=14)
# plt.savefig(output_location+"\swarm_TPG_FP.png")
# plt.show()

# plt.figure(figsize=(6,6))
# sns.swarmplot(data=all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)], x="Sessions", y="player_blue_group_investment", color="b")
# plt.ylabel("Blue Public Good Investment", fontsize = 16)
# plt.ylim(-1,21)
# plt.yticks(ticks=[0,2,4,6,8,10,12,14,16,18,20])
# plt.xlabel("Sessions", fontsize = 16)
# plt.xticks(fontsize=14)
# plt.savefig(output_location+"\swarm_BluePG_FP.png")
# plt.show()

# plt.figure(figsize=(6,6))
# sns.swarmplot(data=all_sessions_df[(all_sessions_df.Treatment == "Multi-Shared") & (all_sessions_df.subsession_round_number == 1)], x="Sessions", y="player_green_group_investment", color="g")
# plt.ylabel("Green Public Good Investment", fontsize = 16)
# plt.ylim(-1,21)
# plt.yticks(ticks=[0,2,4,6,8,10,12,14,16,18,20])
# plt.xlabel("Sessions", fontsize = 16)
# plt.xticks(fontsize=14)
# plt.savefig(output_location+"\swarm_GreenPG_FP.png")
# plt.show()
