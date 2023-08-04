"""
Generate the effect size and function to carry out the power analysis
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================

from constants import np
from constants import TTestIndPower


# ====================================================================================================================
# Power Analysis Constants
# ====================================================================================================================


def gen_effect_size(mean_one: float, mean_two: float, std_dev: float):
  """
  Generate the effect size which is the difference in the treatment means divided by the 'pooled' standard deviation.
  I am assuming the standard deviations are the same which means I divided only by our standard deviation

  :param mean_one: Shared endowment mean investment over the first 5 periods
  :param mean_two: Split endowment (FFG 2013) mean investment over the first 5 periods
  :param std_dev: Standard deviation of players mean investments over the first 5 periods
  :return: the effect size 
  """
  effect_size = (mean_one - mean_two) / std_dev
  return effect_size


def conduct_power_analysis(effect_size: float, alpha: float, power: float):
  """
  Runs the statsmodels power analysis function. For our use case, this determines the number of subjects that we will need to have
  in each treatment.

  :param effect_size: measure of the difference between two treatments | pair-wise
  :param alpha: significance level
  :param power: beta 
  :return: the sample size unrounded.
  """
  power_analysis = TTestIndPower()
  sample_size = power_analysis.solve_power(effect_size = effect_size, 
                                         power = power, 
                                         alpha = alpha)
  return sample_size


def clean_print(sample_size: float):
  """
  Cleanly prints the required sample size for one such treatment rounded up. For our purposes we need to further this to the nearest
  multiple of 16.

  :param sample_size: a simple print statement with a nice message
  """
  print('Required sample size: ', np.ceil(sample_size))