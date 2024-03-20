# %%

# Importing Packages

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams["font.family"] = "Times New Roman"
from datetime import datetime
import os
from extension_utils import (gen_avg_investments, calculate_and_plot_averages,
                             perform_t_tests, perform_non_parametric_tests,
                             plot_averages_all,
                             test_investment_difference_by_round_corrected,
                             calculate_averages,
                             encode_group_investments, encode_additional_group_investments)

# %%

# Logistics

input_folder_ext = r"C:\Users\modak\Dropbox\Work\Multigroup PGG\Data\Extension"
input_folder_main = r"C:\Users\modak\Dropbox\Work\Multigroup PGG\Data\Fall 2023"

today = datetime.now()

output_location = r"C:\Users\modak\Dropbox\Work\Projects\Multigroup PG\Analysis\Output"
path = output_location+"\{}".format(today.strftime('%Y-%m-%d'))

if os.path.exists(path) == False:
    os.mkdir(path)

output_folder = path

# %%

# Data input

main_sessions_df = pd.read_csv(input_folder_main+"\mgpgg_df_all_sessions.csv", index_col=0)
main_session_shared_df = main_sessions_df[main_sessions_df["pgg_treatment_applied"] == "shared"]
main_session_shared_df['bots'] = False
extension_sessions_df = pd.read_csv(input_folder_ext+"\mgpgg_extension_all_data.csv")

# %%

# Data manipulation

# construct min and max group investment for each player in each period (main sessions)

main_session_shared_df['player.max_invest'] = np.where(main_session_shared_df['player.blue_group_investment'] > main_session_shared_df['player.green_group_investment'], 
                                        main_session_shared_df['player.blue_group_investment'], 
                                        main_session_shared_df['player.green_group_investment'])

main_session_shared_df['player.min_invest'] = np.where(main_session_shared_df['player.blue_group_investment'] < main_session_shared_df['player.green_group_investment'], 
                                        main_session_shared_df['player.blue_group_investment'], 
                                        main_session_shared_df['player.green_group_investment'])

main_session_shared_df['max_invest_group'] = np.where(
    main_session_shared_df['player.blue_group_investment'] > main_session_shared_df['player.green_group_investment'], 
    'blue', 
    'green'
)

main_session_shared_df['group_max_invest'] = np.where(
    main_session_shared_df['max_invest_group'] == 'blue',
    main_session_shared_df['player.blue_group_total_investment'],
    main_session_shared_df['player.green_group_total_investment']
)

main_session_shared_df['min_invest_group'] = np.where(
    main_session_shared_df['player.blue_group_investment'] > main_session_shared_df['player.green_group_investment'], 
    'green', 
    'blue'
)

main_session_shared_df['group_min_invest'] = np.where(
    main_session_shared_df['min_invest_group'] == 'blue',
    main_session_shared_df['player.blue_group_total_investment'],
    main_session_shared_df['player.green_group_total_investment']
)

main_avg_max = main_session_shared_df[main_session_shared_df['bots'] == False].groupby('subsession.round_number')['player.max_invest'].mean()
main_avg_min = main_session_shared_df[main_session_shared_df['bots'] == False].groupby('subsession.round_number')['player.min_invest'].mean()

main_avg_blue = main_session_shared_df[main_session_shared_df['bots'] == False].groupby('subsession.round_number')['player.blue_group_investment'].mean()
main_avg_green = main_session_shared_df[main_session_shared_df['bots'] == False].groupby('subsession.round_number')['player.green_group_investment'].mean()

# construct min and max group investment for each player in each period 

copy_extension_sessions_df = extension_sessions_df.copy()

copy_extension_sessions_df['player.max_invest'] = np.where(copy_extension_sessions_df['player.blue_group_investment'] > copy_extension_sessions_df['player.green_group_investment'], 
                                        copy_extension_sessions_df['player.blue_group_investment'], 
                                        copy_extension_sessions_df['player.green_group_investment'])

copy_extension_sessions_df['player.min_invest'] = np.where(copy_extension_sessions_df['player.blue_group_investment'] < copy_extension_sessions_df['player.green_group_investment'], 
                                        copy_extension_sessions_df['player.blue_group_investment'], 
                                        copy_extension_sessions_df['player.green_group_investment'])

copy_extension_sessions_df['max_invest_group'] = np.where(
    copy_extension_sessions_df['player.blue_group_investment'] > copy_extension_sessions_df['player.green_group_investment'], 
    'blue', 
    'green'
)

copy_extension_sessions_df['group_max_invest'] = np.where(
    copy_extension_sessions_df['max_invest_group'] == 'blue',
    copy_extension_sessions_df['player.blue_group_total_investment'],
    copy_extension_sessions_df['player.green_group_total_investment']
)

copy_extension_sessions_df['min_invest_group'] = np.where(
    copy_extension_sessions_df['player.blue_group_investment'] > copy_extension_sessions_df['player.green_group_investment'], 
    'green', 
    'blue'
)

copy_extension_sessions_df['group_min_invest'] = np.where(
    copy_extension_sessions_df['min_invest_group'] == 'blue',
    copy_extension_sessions_df['player.blue_group_total_investment'],
    copy_extension_sessions_df['player.green_group_total_investment']
)

extension_avg_max = copy_extension_sessions_df[copy_extension_sessions_df['bots'] == True].groupby('subsession.round_number')['player.max_invest'].mean()
extension_avg_min = copy_extension_sessions_df[copy_extension_sessions_df['bots'] == True].groupby('subsession.round_number')['player.min_invest'].mean()

extension_avg_blue = copy_extension_sessions_df[copy_extension_sessions_df['bots'] == True].groupby('subsession.round_number')['player.blue_group_investment'].mean()
extension_avg_green = copy_extension_sessions_df[copy_extension_sessions_df['bots'] == True].groupby('subsession.round_number')['player.green_group_investment'].mean()

extension_avg_better, extension_avg_worse = calculate_averages(extension_sessions_df)

# Filter the DataFrame based on 'blue_green' being True or False
df_true = extension_sessions_df[extension_sessions_df['blue_green']]
df_false = extension_sessions_df[~extension_sessions_df['blue_green']]

# Calculate the mean investments for the 'better' and 'worse' groups for both True and False cases
# across all sessions
extension_avg_better_true, extension_avg_worse_true = calculate_averages(df_true)
extension_avg_better_false, extension_avg_worse_false = calculate_averages(df_false)

extension_avg_blue_true = df_true.groupby('subsession.round_number')['player.blue_group_investment'].mean()
extension_avg_green_true = df_true.groupby('subsession.round_number')['player.green_group_investment'].mean()

extension_avg_blue_false = df_false.groupby('subsession.round_number')['player.blue_group_investment'].mean()
extension_avg_green_false = df_false.groupby('subsession.round_number')['player.green_group_investment'].mean()

# %%

main_avg_max_df = main_avg_max.to_frame().reset_index()
main_avg_max_df.rename(columns={"player.max_invest":0}, inplace=True)
main_avg_max_df["Account"] = "Maximum (Main)"
main_avg_min_df = main_avg_min.to_frame().reset_index()
main_avg_min_df.rename(columns={"player.min_invest":0}, inplace=True)
main_avg_min_df["Account"] = "Minimum (Main)"
main_avg_blue_df = main_avg_blue.to_frame().reset_index()
main_avg_blue_df.rename(columns={"player.blue_group_investment":0}, inplace=True)
main_avg_blue_df["Account"] = "Blue (Main)"
main_avg_green_df = main_avg_green.to_frame().reset_index()
main_avg_green_df.rename(columns={"player.green_group_investment":0}, inplace=True)
main_avg_green_df["Account"] = "Green (Main)"

extension_avg_max_df = extension_avg_max.to_frame().reset_index()
extension_avg_max_df.rename(columns={"player.max_invest":0}, inplace=True)
extension_avg_max_df["Account"] = "Maximum (Bots)"
extension_avg_min_df = extension_avg_min.to_frame().reset_index()
extension_avg_min_df.rename(columns={"player.min_invest":0}, inplace=True)
extension_avg_min_df["Account"] = "Minimum (Bots)"
extension_avg_better_df = extension_avg_better.to_frame().reset_index()
extension_avg_better_df["Account"] = "More Cooperative"
extension_avg_worse_df = extension_avg_worse.to_frame().reset_index()
extension_avg_worse_df["Account"] = "Less Cooperative"
extension_avg_blue_df = extension_avg_blue.to_frame().reset_index()
extension_avg_blue_df.rename(columns={"player.blue_group_investment":0}, inplace=True)
extension_avg_blue_df["Account"] = "Blue (Bots)"
extension_avg_green_df = extension_avg_green.to_frame().reset_index()
extension_avg_green_df.rename(columns={"player.green_group_investment":0}, inplace=True)
extension_avg_green_df["Account"] = "Green (Bots)"

extension_avg_better_true_df = extension_avg_better_true.to_frame().reset_index()
extension_avg_better_false_df = extension_avg_better_false.to_frame().reset_index()
extension_avg_worse_true_df = extension_avg_worse_true.to_frame().reset_index()
extension_avg_worse_false_df = extension_avg_worse_false.to_frame().reset_index()

extension_avg_blue_true_df = extension_avg_blue_true.to_frame().reset_index()
extension_avg_blue_true_df.rename(columns={"player.blue_group_investment":0}, inplace=True)
extension_avg_blue_false_df = extension_avg_blue_false.to_frame().reset_index()
extension_avg_blue_false_df.rename(columns={"player.blue_group_investment":0}, inplace=True)
extension_avg_green_true_df = extension_avg_green_true.to_frame().reset_index()
extension_avg_green_true_df.rename(columns={"player.green_group_investment":0}, inplace=True)
extension_avg_green_false_df = extension_avg_green_false.to_frame().reset_index()
extension_avg_green_false_df.rename(columns={"player.green_group_investment":0}, inplace=True)

extension_avg_better_true_df["Order"] = "Blue-Green"
extension_avg_worse_true_df["Order"] = "Blue-Green"
extension_avg_better_false_df["Order"] = "Green-Blue"
extension_avg_worse_false_df["Order"] = "Green-Blue"

extension_avg_better_true_df["Account"] = "More Cooperative"
extension_avg_worse_true_df["Account"] = "Less Cooperative"
extension_avg_better_false_df["Account"] = "More Cooperative"
extension_avg_worse_false_df["Account"] = "Less Cooperative"

extension_avg_blue_true_df["Order"] = "Blue-Green"
extension_avg_green_true_df["Order"] = "Blue-Green"
extension_avg_blue_false_df["Order"] = "Green-Blue"
extension_avg_green_false_df["Order"] = "Green-Blue"

extension_avg_blue_true_df["Account"] = "Blue"
extension_avg_green_true_df["Account"] = "Green"
extension_avg_blue_false_df["Account"] = "Blue"
extension_avg_green_false_df["Account"] = "Green"

combined_avg_df = pd.concat([main_avg_max_df,
                                          main_avg_min_df,
                                          main_avg_blue_df,
                                          main_avg_green_df,
                                          extension_avg_max_df,
                                          extension_avg_min_df,
                                          extension_avg_better_df,
                                          extension_avg_worse_df,
                                          extension_avg_blue_df,
                                          extension_avg_green_df,
                                          extension_avg_better_true_df,
                                          extension_avg_better_false_df,
                                          extension_avg_worse_true_df,
                                          extension_avg_worse_false_df,
                                          extension_avg_blue_true_df,
                                          extension_avg_blue_false_df,
                                          extension_avg_green_true_df,
                                          extension_avg_green_false_df], ignore_index=True)

combined_avg_df.rename(columns={"subsession.round_number":"Period", 0:"Average Account Investment"}, inplace=True)
# print(combined_avg_df)
# %%

g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Maximum (Main)", "Minimum (Main)", "Blue (Main)", "Green (Main)"])], margin_titles=True, hue="Account", hue_kws={"color" : ['k','k','b','g'], "ls" : ["-","--","-","-"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Main_Max_Min_B_G_byPeriod.png', bbox_inches='tight')
plt.show()
# %%

g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Maximum (Bots)", "Minimum (Bots)", "Blue (Bots)", "Green (Bots)"])], margin_titles=True, hue="Account", hue_kws={"color" : ['k','k','b','g'], "ls" : ["-","--","-","-"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Bots_Max_Min_B_G_byPeriod.png', bbox_inches='tight')
# %%

g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Maximum (Bots)", "Minimum (Bots)", "More Cooperative", "Less Cooperative"])], margin_titles=True, hue="Account", hue_kws={"color" : ['k','k','r','r'], "ls" : ["-","--","-","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Bots_Max_Min_M_L_byPeriod.png', bbox_inches='tight')
# %%

g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Maximum (Bots)", "Minimum (Bots)", "Maximum (Main)", "Minimum (Main)"])], margin_titles=True, hue="Account", hue_kws={"color" : ['r','r','k','k'], "ls" : ["-","--","-","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Max_Min_byPeriod.png', bbox_inches='tight')

# %%

g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Blue (Bots)", "Green (Bots)", "Blue (Main)", "Green (Main)"])], margin_titles=True, hue="Account", hue_kws={"color" : ['b','g','b','g'], "ls" : ["-","-","--","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\B_G_byPeriod.png', bbox_inches='tight')


# %%

# Order effects

df_1 = combined_avg_df[combined_avg_df.Order.isin(["Green-Blue", "Blue-Green"])]

g = sns.FacetGrid(df_1[df_1.Account.isin(["More Cooperative", "Less Cooperative"])], col="Order", margin_titles=True, hue="Account", hue_kws={"color" : ['k', 'k'], "ls" : ["-","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
# loc='lower center', bbox_to_anchor=(0.35, -0.2), ncols=2
g.add_legend(loc='lower center', bbox_to_anchor=(0.4, -0.2), ncols=2)
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=16)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Order_Effect_M_L_byPeriod.png', bbox_inches='tight')

g = sns.FacetGrid(df_1[df_1.Account.isin(["Green", "Blue"])], col="Order", margin_titles=True, hue="Account", hue_kws={"color" : ['b', 'g'], "ls" : ["-","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Account Investment")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='lower center', bbox_to_anchor=(0.4, -0.2), ncols=2)
g.legend.set_title("Account")
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=16)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Order_Effect_B_G_byPeriod.png', bbox_inches='tight')

# %%

main_personal = main_session_shared_df.groupby('subsession.round_number')['player.personal_account'].mean()
extension_personal = extension_sessions_df.groupby('subsession.round_number')['player.personal_account'].mean()

main_personal_df = main_personal.to_frame().reset_index()
main_personal_df.rename(columns={"player.personal_account":0}, inplace=True)
main_personal_df["Sessions"] = "Main"
extension_personal_df = extension_personal.to_frame().reset_index()
extension_personal_df.rename(columns={"player.personal_account":0}, inplace=True)
extension_personal_df["Sessions"] = "Bots"

combined_personal_avg_df = pd.concat([main_personal_df, extension_personal_df], ignore_index=True)

combined_personal_avg_df.rename(columns={"subsession.round_number":"Period", 0:"Average Amount in Personal Account"}, inplace=True)
# print(combined_personal_avg_df)

# %%

g = sns.FacetGrid(combined_personal_avg_df, margin_titles=True, hue="Sessions", hue_kws={"color" : ['k','k'], "ls" : ["-","--"]}, height=4, aspect=1.5)
g.map(sns.lineplot, "Period", "Average Amount in Personal Account")
# g.map(plt.fill_between, "Supergame", "Bootstrap LCI", "Bootstrap HCI", alpha = 0.2)
g.set_titles(col_template = '{col_name}', size=16)
g.set_ylabels(fontsize=14)
g.set_xlabels("Period", fontsize=14)
g.set(xlim=(1, 20), ylim=(0, 20), xticks=[1, 5, 10, 15, 20])
g.add_legend(loc='center right', bbox_to_anchor=(1.05, 0.5))
plt.setp(g._legend.get_title(), fontsize=16)
plt.setp(g._legend.get_texts(), fontsize=14)
for ax in g.axes.flatten():
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
plt.savefig(output_folder+'\Personal_Compare_byPeriod.png', bbox_inches='tight')

# %%
