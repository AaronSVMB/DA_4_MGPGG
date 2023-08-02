"""
Useful constants for various aspects of the DA 
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================

import math
import pandas as pd
import numpy as np 
import scipy.stats as stats
import matplotlib.pyplot as plt


# ====================================================================================================================
# Strategy Method Constants
# ====================================================================================================================


conditional_investment_list = ['player.conditional_investment_0','player.conditional_investment_1',
                               'player.conditional_investment_2','player.conditional_investment_3',
                               'player.conditional_investment_4','player.conditional_investment_5',
                               'player.conditional_investment_6','player.conditional_investment_7',
                               'player.conditional_investment_8','player.conditional_investment_9',
                               'player.conditional_investment_10','player.conditional_investment_11',
                               'player.conditional_investment_12','player.conditional_investment_13',
                               'player.conditional_investment_14','player.conditional_investment_15',
                               'player.conditional_investment_16','player.conditional_investment_17',
                               'player.conditional_investment_18','player.conditional_investment_19',
                               'player.conditional_investment_20']

conditional_investment_x_values = [x for x in range(0,21)]

# FR, CC, HS, OT for player-typing order
fgf_distribution = np.array([13, 22, 6, 3])  # 44 subjs
fgq_distrubtion = np.array([32, 77, 17, 14])  # 140 subjs
