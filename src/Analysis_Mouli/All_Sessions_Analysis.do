* Importing Data

clear

import delimited "C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Input\all_sessions_treatment_strategy.csv"

* Data Wrangling

drop v1 unnamed0

** Encoding treatment

encode treatment, generate(treatment_code)
label define treatment_code 1 "Single Group", modify
label define treatment_code 2 "Multi-Split", modify
label define treatment_code 3 "Multi-Shared", modify
label define treatment_code 4 "Multi-Shared Bots", modify
drop treatment_code
encode treatment, generate(treatment_code)

** Encoding participant id

encode participant_code, generate(participant_ID)

** Panel Data

xtset participant_ID subsession_round_number

** Tobit Data/Restrictions -- Investment

gen ul_inv = 20
replace ul_inv = 10 if treatment_code == 2
gen ll_inv = 0

** Difference Data

gen diff_inv = player_blue_group_investment - player_green_group_investment
gen diff_group = player_others_blue_group_investm - player_others_green_group_invest
gen lag_diff_group = l_player_others_blue_group_inves - l_player_others_green_group_inve
gen lag_diff_inv = L.diff_inv

** Tobit Data/Restrictions -- Difference in Investments

gen ul_diff = 20
replace ul_diff = 10 if treatment_code == 2
gen ll_diff = -20
replace ll_diff = -10 if treatment_code == 2

*-----------------------------------------------------------------------------------------*

* Regressions

** Effect of Treatment on Investments (All Periods)

xttobit player_total_pgg_investment i.treatment_code, ll(ll_inv ) ul(ul_inv ) re // robust standards are not working

*** Test

testnl (_b[player_total_pgg_investment :2.treatment_code] == _b[player_total_pgg_investment :3.treatment_code]) (_b[player_total_pgg_investment :2.treatment_code] == _b[player_total_pgg_investment :4.treatment_code]) (_b[player_total_pgg_investment :3.treatment_code] == _b[player_total_pgg_investment :4.treatment_code]), mtest(bonferroni)

** Effect of Treatment on Investments with Trend (All Periods)

xttobit player_total_pgg_investment i.treatment_code i.treatment_code#c.subsession_round_number, ll(ll_inv ) ul(ul_inv ) re

*** Test

testnl (_b[player_total_pgg_investment :2.treatment_code] == _b[player_total_pgg_investment :3.treatment_code]) (_b[player_total_pgg_investment :2.treatment_code] == _b[player_total_pgg_investment :4.treatment_code]) (_b[player_total_pgg_investment :3.treatment_code] == _b[player_total_pgg_investment :4.treatment_code]), mtest(bonferroni)

** Effect of Treatment on Investments (First Period)

tobit player_total_pgg_investment i.treatment_code if subsession_round_number == 1, ll(ll_inv) ul(ul_inv) vce(robust)
tobit player_blue_group_investment i.treatment_code if subsession_round_number == 1, ll(ll_inv) ul(ul_inv) vce(robust)
tobit player_green_group_investment i.treatment_code if subsession_round_number == 1, ll(ll_inv) ul(ul_inv) vce(robust)

** Effect of Last period diff in group investments on Diff in current investment by treatment

xttobit diff_inv i.treatment_code i.treatment_code#c.lag_diff_group if treatment_code != 1, ul(ul_diff) ll(ll_diff) re

*** Test

testnl (_b[diff_inv:2.treatment_code#c.lag_diff_group] == _b[diff_inv:3.treatment_code#c.lag_diff_group] == _b[diff_inv:4.treatment_code#c.lag_diff_group]), mtest(bonferroni)

** Effect of Last period diff in group investments on Diff in current investment by treatment (autoregression)

xttobit diff_inv i.treatment_code i.treatment_code#c.lag_diff_group i.treatment_code#c.lag_diff_inv if treatment_code != 1, ul(ul_diff) ll(ll_diff) re

*** Test

testnl (_b[diff_inv:2.treatment_code#c.lag_diff_group] == _b[diff_inv:3.treatment_code#c.lag_diff_group] == _b[diff_inv:4.treatment_code#c.lag_diff_group]), mtest(bonferroni)

