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
# Holt Laury (2002) Constants
# ====================================================================================================================


# upper-bounds of the risk estimation 
risk_estimation_upper_dict = {
    0: -0.95,
    1: -0.95,
    2: -0.49,
    3: -0.15,
    4: 0.15,
    5: 0.41,
    6: 0.68,
    7: 0.97,
    8: 1.37,
    9: float('inf'),
    10: float('inf')
}

# lower-bounds of the risk estimation 
risk_estimation_lower_dict = {
    0: float('-inf'),
    1: float('-inf'),
    2: -0.95,
    3: -0.49,
    4: -0.15,
    5: 0.15,
    6: 0.41,
    7: 0.68,
    8: 0.97,
    9: 1.37,
    10: 1.37
}

# risk classifcaitons
risk_classifcations_dict = {
    0: 'highly risk loving',
    1: 'hightly risk loving',
    2: 'very risk loving',
    3: 'risk loving',
    4: 'risk neutral',
    5: 'slightly risk average',
    6: 'risk averse',
    7: 'very risk averse',
    8: 'highly risk averse',
    9: 'stay in bed',
    10: 'stay in bed'
}