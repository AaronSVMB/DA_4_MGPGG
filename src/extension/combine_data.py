# Importing packages

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
from extension_utils import (extension_reading_and_cleaning, 
                             extension_merge_game_and_instrucs,
                             extension_merge_game_and_survey)

# Folder name for storing data

foldername = ""

# Loading data

extension_data_week_one_bg = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/bots_shared_rounds_nov3.csv')
extension_data_week_two_bg = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/final/bots_shared_2023-11-19.csv')
all_gb_data = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/week_two/bots_shared_flipped_2023-11-10.csv')

# Combine Blue-Green Screen data and add binary column showing this 'treatment' // control

all_bg_data = pd.concat([extension_data_week_one_bg, extension_data_week_two_bg], ignore_index=True)
all_bg_data['blue_green'] = True

# 0 for the green-blue df

all_gb_data['blue_green'] = False

# combine the two bg and gb data frame

mgpgg_extension_df = pd.concat([all_bg_data, all_gb_data], ignore_index=True)

# Add instructions

extension_week_one_instrucs_bg = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/bots_shared_instrucs_nov3.csv')
extension_week_two_instrucs_bg = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/final/bots_shared_instrucs_2023-11-19.csv')
all_gb_df = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/week_two/bots_shared_flipped_instrucs_2023-11-10.csv')

mgpgg_extension_instrucs_df = pd.concat([extension_week_one_instrucs_bg, extension_week_two_instrucs_bg, all_gb_df], ignore_index=True)

# Combine treatment and instruc data

mgpgg_extension_game_and_instrucs_df = extension_merge_game_and_instrucs(mgpgg_extension_df, mgpgg_extension_instrucs_df)

# Add survey q answers

extension_survey_week_one_df = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/bots_multi_survey_nov3.csv')
extension_survey_week_two_bg_df = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/final/bots_multi_survey_2023-11-19.csv')
extension_survey_week_two_gb_df = extension_reading_and_cleaning('/Users/aaronberman/Desktop/DA_4_MGPGG/src/extension/bots_data/week_two/bots_multi_flipped_survey_2023-11-10.csv')

extension_survey_df = pd.concat([extension_survey_week_one_df, extension_survey_week_two_bg_df, extension_survey_week_two_gb_df], ignore_index=True)

mgpgg_extension_all_df = extension_merge_game_and_survey(mgpgg_extension_game_and_instrucs_df, extension_survey_df)
mgpgg_extension_all_df['bots'] = True

print(mgpgg_extension_all_df.head())

mgpgg_extension_all_df.to_csv(foldername+'mgpgg_extension_all_data.csv', index=False)