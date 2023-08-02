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

### Pathing 

"export PYTHONPATH=$PYTHONPATH:./src"