"""
Functions to perform various regressions on our MGPGG data    
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd
import statsmodels.api as sm
import linearmodels
from linearmodels import PanelOLS


# ====================================================================================================================
# panel ols
# ====================================================================================================================


def gen_panel_ols(df: pd.DataFrame, indices: list, depVar: str, indepVar):
    """generates standard panel data ols results

    :param df: mgpggdf all apps
    :param indices: fixed effects
    :param depVar: metric of interest
    :param indepVar: explanatory variables
    """
    df = df.set_index(indices)

    y = df.loc[:, depVar]

    X = df.loc[:, indepVar]

    X = sm.add_constant(X)

    model = PanelOLS(y, X, entity_effects=True)

    result = model.fit()

    print(result)