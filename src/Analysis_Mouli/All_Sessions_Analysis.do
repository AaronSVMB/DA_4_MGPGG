* Importing Data

clear

import delimited "C:\Users\mouli\Dropbox\Work\Projects\Multigroup PG\Analysis\Input\mgpgg_all_data_df.csv"

* Data Wrangling

// drop v1 unnamed0

** Encoding treatment

replace treatment = "Multi-Shared (Human)" if treatment == "Multi-Shared"
replace treatment = "Multi-Shared (Bots Unbalanced)" if treatment == "Bots Unbalanced"
replace treatment = "Multi-Shared (Bots Balanced)" if treatment == "Bots Balanced"
// encode treatment, generate(treatment_code)
label define treatment_code 1 "Single Group", modify
label define treatment_code 2 "Multi-Split", modify
label define treatment_code 3 "Multi-Shared (Human)", modify
label define treatment_code 4 "Multi-Shared (Bots Balanced)", modify
label define treatment_code 5 "Multi-Shared (Bots Unbalanced)", modify
// drop treatment_code
encode treatment, generate(treatment_code)

** Encoding participant id

encode participant_code, generate(participant_ID)

** Panel Data

xtset participant_ID period

** Tobit Data/Restrictions -- Investment

gen ul_inv = 20
replace ul_inv = 10 if treatment_code == 2
gen ll_inv = 0

** Difference Data

gen diff_inv = blue_investment - green_investment
gen blue_other_investment = blue_total_invest - blue_investment
gen green_other_investment = green_total_invest - green_investment
gen diff_group = blue_other_investment - green_other_investment
gen lag_diff_group = L.diff_group
gen lag_diff_inv = L.diff_inv

** Total investment

gen total_pgg_investment = investment if treatment_code == 1
replace total_pgg_investment = blue_investment + green_investment if treatment_code != 1

** Tobit Data/Restrictions -- Difference in Investments

gen ul_diff = 20
replace ul_diff = 10 if treatment_code == 2
gen ll_diff = -20
replace ll_diff = -10 if treatment_code == 2

*-----------------------------------------------------------------------------------------*

* Regressions

** Effect of Treatment on Investments (All Periods)

xttobit total_pgg_investment i.treatment_code, ll(ll_inv ) ul(ul_inv ) re // robust standards are not working

*** Test

** Testing if splitting helps in increasing overall investments

testnl (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :2.treatment_code]) (_b[total_pgg_investment: 1.treatment_code] == _b[total_pgg_investment :3.treatment_code]) (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :4.treatment_code]) (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :5.treatment_code]), mtest(bonferroni)

** Testing if split and shared have the same effect

testnl (_b[total_pgg_investment :2.treatment_code] == _b[total_pgg_investment :3.treatment_code]), mtest(bonferroni)

** Testing the effect of shared with humans and non-humans

testnl (_b[total_pgg_investment :3.treatment_code] == _b[total_pgg_investment :4.treatment_code]) (_b[total_pgg_investment :3.treatment_code] == _b[total_pgg_investment :5.treatment_code]) (_b[total_pgg_investment :4.treatment_code] == _b[total_pgg_investment :5.treatment_code]), mtest(bonferroni)

** Effect of Treatment on Investments with Trend (All Periods)

xttobit total_pgg_investment i.treatment_code i.treatment_code#c.period, ll(ll_inv ) ul(ul_inv ) re

*** Test

** Testing if splitting helps in increasing overall investments

testnl (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :2.treatment_code]) (_b[total_pgg_investment: 1.treatment_code] == _b[total_pgg_investment :3.treatment_code]) (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :4.treatment_code]) (_b[total_pgg_investment :1.treatment_code] == _b[total_pgg_investment :5.treatment_code]), mtest(bonferroni)

** Testing if split and shared have the same effect

testnl (_b[total_pgg_investment :2.treatment_code] == _b[total_pgg_investment :3.treatment_code]), mtest(bonferroni)

** Testing the effect of shared with humans and non-humans

testnl (_b[total_pgg_investment :3.treatment_code] == _b[total_pgg_investment :4.treatment_code]) (_b[total_pgg_investment :3.treatment_code] == _b[total_pgg_investment :5.treatment_code]) (_b[total_pgg_investment :4.treatment_code] == _b[total_pgg_investment :5.treatment_code]), mtest(bonferroni)

** Effect of Treatment on Investments (First Period)

tobit total_pgg_investment i.treatment_code if period == 1, ll(ll_inv) ul(ul_inv) vce(robust)
tobit player_blue_group_investment i.treatment_code if period == 1, ll(ll_inv) ul(ul_inv) vce(robust)
tobit player_green_group_investment i.treatment_code if period == 1, ll(ll_inv) ul(ul_inv) vce(robust)

** Effect of Last period diff in group investments on Diff in current investment by treatment

xttobit diff_inv i.treatment_code i.treatment_code#c.lag_diff_group if treatment_code != 1, ul(ul_diff) ll(ll_diff) re

*** Test

testnl (_b[diff_inv:2.treatment_code#c.lag_diff_group] == _b[diff_inv:3.treatment_code#c.lag_diff_group] == _b[diff_inv:4.treatment_code#c.lag_diff_group]), mtest(bonferroni)

** Effect of Last period diff in group investments on Diff in current investment by treatment (autoregression)

xttobit diff_inv i.treatment_code i.treatment_code#c.lag_diff_group i.treatment_code#c.lag_diff_inv if treatment_code != 1, ul(ul_diff) ll(ll_diff) re

*** Test

testnl (_b[diff_inv:2.treatment_code#c.lag_diff_group] == _b[diff_inv:3.treatment_code#c.lag_diff_group] == _b[diff_inv:4.treatment_code#c.lag_diff_group]), mtest(bonferroni)

