# Purpose

This is code for the subsequent data analysis to be run for the MGPGG. The analysis comes in multiple sections. There is code to analyze the data for the Treatments (standard pgg, split endowment, shared endowment), and for the strategy method (as seen in FGF (2000)).

## Treatment Analysis

## Strategy Method Analysis

These classifications are done as described by FGF (2000) and FGQ (2012) 

Rules for classification 
- Conditional cooperators CC - all subjects who show either a monotonic pattern with at least one increase or who have a positive spearman rank correlation that is significant at the `% level
- Free-riders – All subjects who contribute 0 to all cases
- Hump / Triangle contributors – subjects who have a significant increase scheme up to some maximum and a significant decrease thereafter again using spearman rank correlation at 1% level for both.
- Other – all subjects who cannot be classified in this way

Post-classification tests
- ‘We find that the distribution of preference types is the same across all six independent session (fisher exact test) ==> This allows them to pool the data from all sessions
- Robustness Check: with FGF data – chi square cannot reject the null hypothesis of equal distribution of types. 

I implemented both

## Risk Preference – Holt and Laury (2002) – Analysis

Goal. Produce metric of risk aversion for each player based on their Risk Preference choices.

The general idea is the num_times_choose_A (Safe lottery) Inc = Inc Risk Aversion = Inc r estimation interval
    where r = 0 risk neutral, r less than 0 risk seeking, and r > 0 risk averse.
    Given the utility function U(x) = x^(1-r)/(1-r).

Our values for A and B have the same switching point as Holt and Laury (2002) so I can take advantage of the risk estimation intervals that they construct from the aforementioned utility function.

The Risk Preference Code
- Reads and cleans the risk preference data
- Counts the number of times each subject selects the safe lottery, A, and stores this value
- Produces an upper and lower bound for the risk estimate based off the above
- Classifies the player on a risk scale
- Produces summary statistics on the Risk Preferences across sessions
- A simple bar chart to visualize the distribution of this content

### Pathing 

"export PYTHONPATH=$PYTHONPATH:./src"