import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "Times New Roman"
from data_wrangling_functions import grouping_diff_others_investment

def plot_count_data(data_figure, periods, account, sessions, output_location):
    
    if account == "Total":

        plt.figure(figsize=(16,8))

        if sessions == "main":
            # plt.figure(figsize=(12,8))
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_total_PGG_investment", y="proportion", hue="Treatment", edgecolor="0.5", palette=["#191919","#666","#999"])
        elif sessions == "bots":
            if periods == "AP":
                data = data_figure["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1]["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_total_PGG_investment", y="proportion", color = "#ccc", edgecolor="0.5")
        elif sessions == "both":
            hue_order = ["Single Group", "Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_total_PGG_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_total_PGG_investment", y="proportion", hue="Treatment", edgecolor="0.5", hue_order=hue_order, palette=["#191919","#666","#999","#ccc"])
        # print(data)
        
        plt.xlabel("Total Public Good Investment", fontsize = 16)
        plt.ylabel("Relative Frequency", fontsize = 16)
        plt.ylim(0,np.max(data["proportion"]) + 0.01)
        # plt.xticks(ticks=range(21), labels=range(21))
        plt.grid(axis="y")
        plt.savefig(output_location+'\CountPlot_Total_{}_{}_Sessions.png'.format(periods, sessions), bbox_inches='tight')
        plt.show()

    elif account == "Blue":

        plt.figure(figsize=(12,8))

        if sessions == "main":
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_blue_group_investment", y="proportion", hue="Treatment", palette=["#000165", "#0103fd"], edgecolor="0.5")
        elif sessions == "bots":
            if periods == "AP":
                data = data_figure["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1]["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_blue_group_investment", y="proportion", color = "#96b3d1", edgecolor="0.5")
        elif sessions == "both":
            hue_order = ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_blue_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_blue_group_investment", y="proportion", hue="Treatment", hue_order=hue_order, palette=["#000165", "#0103fd", "#96b3d1"], edgecolor="0.5")
        
        plt.xlabel("Blue Public Good Investment", fontsize = 16)
        plt.ylabel("Relative Frequency", fontsize = 16)
        plt.ylim(0,np.max(data["proportion"]) + 0.01)
        # plt.xticks(ticks=range(21), labels=range(21))
        plt.grid(axis="y")
        plt.savefig(output_location+'\CountPlot_Blue_{}_{}_Sessions.png'.format(periods, sessions), bbox_inches='tight')
        plt.show()

    elif account == "Green":

        plt.figure(figsize=(12,8))

        if sessions == "main":
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_green_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_green_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_green_group_investment", y="proportion", hue="Treatment", palette=["#01310f", "#03952f"], edgecolor="0.5")
        elif sessions == "bots":
            if periods == "AP":
                data = data_figure["player_green_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1]["player_green_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_green_group_investment", y="proportion", color="#06f84e", edgecolor="0.5")
        elif sessions == "both":
            hue_order = ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
            if periods == "AP":
                data = data_figure.groupby("Treatment")["player_green_group_investment"].value_counts(normalize=True).reset_index()
            else:
                data = data_figure[data_figure.subsession_round_number == 1].groupby("Treatment")["player_green_group_investment"].value_counts(normalize=True).reset_index()
            sns.barplot(data, x="player_green_group_investment", y="proportion", hue="Treatment", hue_order=hue_order, palette=["#01310f", "#03952f", "#06f84e"], edgecolor="0.5")
        # print(data)
        
        plt.xlabel("Green Public Good Investment", fontsize = 16)
        plt.ylabel("Relative Frequency", fontsize = 16)
        plt.ylim(0,np.max(data["proportion"]) + 0.01)
        # plt.xticks(ticks=range(21), labels=range(21))
        plt.grid(axis="y")
        plt.savefig(output_location+'\CountPlot_Green_{}_{}_Sessions.png'.format(periods, sessions), bbox_inches='tight')
        plt.show()

    # Distribution comparison

    # stat01, pval01 = stats.kruskal(data[data.Treatment == "Single Group"]["player_total_PGG_investment"], data[data.Treatment == "Multi-Split"]["player_total_PGG_investment"])
    # print("Single vs. Split: ", round(pval01,3))
    # stat02, pval02 = stats.kruskal(data[data.Treatment == "Single Group"]["player_total_PGG_investment"], data[data.Treatment == "Multi-Shared"]["player_total_PGG_investment"])
    # print("Single vs. Shared: ", round(pval02,3))
    # stat12, pval12 = stats.kruskal(data[data.Treatment == "Multi-Split"]["player_total_PGG_investment"], data[data.Treatment == "Multi-Shared"]["player_total_PGG_investment"])
    # print("Split vs. Shared: ", round(pval12,3))

    # stat12B, pval12B = stats.kruskal(data[data.Treatment == "Multi-Split"]["Player Blue Investment"], data[data.Treatment == "Multi-Shared"]["Player Blue Investment"])
    # print("Split Blue vs. Shared Blue: ", round(pval12B, 3))
    # stat12G, pval12G = stats.kruskal(data[data.Treatment == "Multi-Split"]["Player Green Investment"], data[data.Treatment == "Multi-Shared"]["Player Green Investment"])
    # print("Split Green vs. Shared Green: ", round(pval12G, 3))
    # stat1BG, pval1BG = stats.kruskal(data[data.Treatment == "Multi-Split"]["Player Blue Investment"], data[data.Treatment == "Multi-Split"]["Player Green Investment"])
    # print("Split Blue vs. Split Green: ", round(pval1BG, 3))
    # stat2BG, pval2BG = stats.kruskal(data[data.Treatment == "Multi-Shared"]["Player Blue Investment"], data[data.Treatment == "Multi-Shared"]["Player Green Investment"])
    # print("Shared Blue vs. Shared Green: ", round(pval2BG, 3))
    
def plot_avg_amount_account_byPeriod(data_figure, account, sessions, output_location):
    
    plt.figure(figsize=(7,6))
    
    if account == "Total":
        hue_order = ["Single Group", "Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
        data = data_figure.groupby(["Treatment", "subsession_round_number"])["player_total_PGG_investment"].mean().reset_index()
        sns.lineplot(data, x="subsession_round_number", y="player_total_PGG_investment", hue="Treatment", hue_order=hue_order, palette=["#191919","#666","#999","#ccc"], style="Treatment")
        plt.ylabel("Average Total\nPublic Good Investment", fontsize = 16)
        plt.legend()
    elif account == "Blue":
        hue_order = ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
        data = data_figure.groupby(["Treatment", "subsession_round_number"])["player_blue_group_investment"].mean().reset_index()
        sns.lineplot(data[data.Treatment != "Single Group"], x="subsession_round_number", y="player_blue_group_investment", hue="Treatment", hue_order=hue_order, palette=["#000165", "#0103fd", "#96b3d1"], style="Treatment")
        plt.ylabel("Average Blue\nPublic Good Investment", fontsize = 16)
        plt.legend()
    elif account == "Green":
        hue_order = ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
        data = data_figure.groupby(["Treatment", "subsession_round_number"])["player_green_group_investment"].mean().reset_index()
        sns.lineplot(data[data.Treatment != "Single Group"], x="subsession_round_number", y="player_green_group_investment", hue="Treatment", hue_order=hue_order, palette=["#01310f", "#03952f", "#06f84e"], style="Treatment")
        plt.ylabel("Average Green\nPublic Good Investment", fontsize = 16)
        plt.legend()
    elif account == "Personal":
        hue_order = ["Single Group", "Multi-Split", "Multi-Shared", "Multi-Shared Bots"]
        data = data_figure.groupby(["Treatment", "subsession_round_number"])["player_personal_account"].mean().reset_index()
        sns.lineplot(data, x="subsession_round_number", y="player_personal_account", hue="Treatment", hue_order=hue_order, palette=["#191919","#666","#999","#ccc"], style="Treatment")
        plt.ylabel("Average Personal Account Amount", fontsize = 16)  
        plt.legend()
    
    plt.xlabel("Period", fontsize = 16)    
    plt.ylim(0,20)
    plt.xticks(ticks=[1,5,10,15,20])
    plt.grid(linestyle='--', linewidth=0.5)
    plt.savefig(output_location+'\AvgInv_ByPeriod_{}_{}_Sessions.png'.format(account, sessions), bbox_inches='tight')
    plt.show()
    
def plot_diff_BlueGreen(data_figure, output_location):
    
    data_figure["diff_player_group_investment"] = data_figure["player_blue_group_investment"] - data_figure["player_green_group_investment"]
    data_figure["L_diff_others_group_investment"] = (data_figure["L_player_others_blue_group_investment"] - data_figure["L_player_others_green_group_investment"])/3
    data_figure["player_more_blue_investment"] = np.where(data_figure["diff_player_group_investment"] > 0, 1, 0)
    data_figure["player_more_green_investment"] = np.where(data_figure["diff_player_group_investment"] < 0, 1, 0)
    data_figure["player_equal_blue_green_investment"] = np.where(data_figure["diff_player_group_investment"] == 0, 1, 0)
    data_figure["others_more_blue_investment"] = np.where(data_figure["L_diff_others_group_investment"] > 0, 1, 0)
    data_figure["others_more_green_investment"] = np.where(data_figure["L_diff_others_group_investment"] < 0, 1, 0)
    data_figure["others_equal_blue_green_investment"] = np.where(data_figure["L_diff_others_group_investment"] == 0, 1, 0)
    data_figure['range_L_diff_others_group_investment']=data_figure.apply(lambda row : grouping_diff_others_investment(row), axis=1)
    
    # print(data_figure[(data_figure.Treatment  != "Single Group") & (data_figure.subsession_round_number ==3)][["Treatment", "L_diff_others_group_investment", "diff_player_group_investment"]].head(10))
    
    for treatment in ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]:
        
        plt.figure(figsize=(6,6))
        
        data = data_figure[data_figure.Treatment == treatment]
    
        sns.lineplot(data = data, x = "L_diff_others_group_investment", y= "diff_player_group_investment", color='k')
    
        plt.ylabel("Difference in Investment (Blue - Green)", fontsize=16)
        plt.xlabel("Difference in Others' Investment in Last Period\n(Blue - Green)", fontsize=16)
        plt.axhline(y=0, color = "k")
        plt.axvline(x=0, color = "k")
        plt.xlim(-20, 20)
        plt.ylim(-20, 20)
        plt.grid(linestyle='--', linewidth=0.5)
        plt.savefig(output_location+'\Difference_Account_Investment_{}.png'.format(treatment), bbox_inches='tight')
        plt.show()
    
    
        sns.lineplot(data = data, x="range_L_diff_others_group_investment", y="player_more_blue_investment", color='b', label="More Invested in Blue")
        sns.lineplot(data = data, x="range_L_diff_others_group_investment", y="player_more_green_investment", color='g', label="More Invested in Green")
        sns.lineplot(data = data, x="range_L_diff_others_group_investment", y="player_equal_blue_green_investment", color='k', label="Equal Investment")
        plt.ylim(-0.02,1.02)
        plt.xticks([1,2,3,4,5,6,7,8,9], labels = ["[-20, -15)","[-15, -10)", "[-10, -5)", "[-5, 0)", "0", "(0, 5]", "(5, 10]", "(10, 15]", "(15, 20]"])
        # plt.xticklabel()
        plt.ylabel("Relative Frequency", fontsize=16)
        plt.xlabel("Difference in Others' Average Investment in Last Period\n(Blue - Green)", fontsize=16)
        plt.grid(linestyle='--', linewidth=0.5)
        # plt.titles(col_template = '',size = 14)
        # g.add_legend()
        # plt.setp(g._legend.get_title(), fontsize=12)
        # for ax in g.axes.flatten():
        #     ax.grid(True, which='both', linestyle='--', linewidth=0.5)
        plt.savefig(output_location+'\Prob_Diff_Account_Investment_{}.png'.format(treatment), bbox_inches='tight')
        plt.show()

def plot_avg_inv_diffaccount_byPeriod(data_figure, column_list, color_list, style_list, label_list, accounts, output_location):

    # print(label_list)

    for treatment in ["Multi-Split", "Multi-Shared", "Multi-Shared Bots"]:
        
        plt.figure(figsize=(6,6))
        
        data = data_figure[data_figure.Treatment == treatment]

        for i, column in enumerate(column_list):

            sns.lineplot(data = data, x = "subsession_round_number", y= data[column], color=color_list[i], linestyle = style_list[i], label=label_list[i], errorbar=None)
            # print(label_list[i])
        
        plt.ylabel("Average Public Good Investment", fontsize=16)
        plt.xlabel("Period", fontsize=16)
        plt.ylim(0,20)
        plt.xticks(ticks=[1,5,10,15,20])
        plt.grid(linestyle='--', linewidth=0.5)
        plt.savefig(output_location+'\AvgInv_ByPeriod_{}_{}.png'.format(accounts, treatment), bbox_inches='tight')
        plt.show()

def plot_order_effect(data_figure, output_location):

    print(data_figure['blue_green'])

    # Filter the DataFrame based on 'blue_green' being True or False
    df_true = data_figure[data_figure['blue_green'] == True]
    df_false = data_figure[data_figure['blue_green'] == False]

    extension_avg_blue_true = df_true.groupby('subsession_round_number')['player_blue_group_investment'].mean()
    extension_avg_green_true = df_true.groupby('subsession_round_number')['player_green_group_investment'].mean()

    extension_avg_blue_false = df_false.groupby('subsession_round_number')['player_blue_group_investment'].mean()
    extension_avg_green_false = df_false.groupby('subsession_round_number')['player_green_group_investment'].mean()

    extension_avg_blue_true_df = extension_avg_blue_true.to_frame().reset_index()
    extension_avg_blue_true_df.rename(columns={"player_blue_group_investment":0}, inplace=True)
    extension_avg_blue_false_df = extension_avg_blue_false.to_frame().reset_index()
    extension_avg_blue_false_df.rename(columns={"player_blue_group_investment":0}, inplace=True)
    extension_avg_green_true_df = extension_avg_green_true.to_frame().reset_index()
    extension_avg_green_true_df.rename(columns={"player_green_group_investment":0}, inplace=True)
    extension_avg_green_false_df = extension_avg_green_false.to_frame().reset_index()
    extension_avg_green_false_df.rename(columns={"player_green_group_investment":0}, inplace=True)

    extension_avg_blue_true_df["Order"] = "Blue-Green"
    extension_avg_green_true_df["Order"] = "Blue-Green"
    extension_avg_blue_false_df["Order"] = "Green-Blue"
    extension_avg_green_false_df["Order"] = "Green-Blue"

    extension_avg_blue_true_df["Account"] = "Blue"
    extension_avg_green_true_df["Account"] = "Green"
    extension_avg_blue_false_df["Account"] = "Blue"
    extension_avg_green_false_df["Account"] = "Green"

    print(extension_avg_blue_false_df)

    combined_avg_df = pd.concat([extension_avg_blue_false_df, extension_avg_blue_true_df, extension_avg_green_false_df, extension_avg_green_true_df], ignore_index=True)
 
    combined_avg_df.rename(columns={"subsession_round_number":"Period", 0:"Average Account Investment"}, inplace=True)

    g = sns.FacetGrid(combined_avg_df[combined_avg_df.Account.isin(["Green", "Blue"])], col="Order", margin_titles=True, hue="Account", hue_kws={"color" : ['b', 'g'], "ls" : ["-","--"]}, height=4, aspect=1.5)
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
    plt.savefig(output_location+'\Order_Effect_B_G_byPeriod.png', bbox_inches='tight')
    plt.show()