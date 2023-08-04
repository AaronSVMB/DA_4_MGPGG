"""
Useful constants for the power analysis
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================

import pandas as pd
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import math
from statsmodels.stats.power import TTestIndPower


# ====================================================================================================================
# Power Analysis Constants
# ====================================================================================================================

# Params (data from FFG 2013)
FFG_avg_invest_1_to_5 = 11.3
FFG_avg_invest_1_to_5_as_perc = 11.3 / 40

# Alpha
alpha = 0.05
# Beta
power = 0.8