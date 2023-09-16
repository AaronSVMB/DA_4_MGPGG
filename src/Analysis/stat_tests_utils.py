"""
Functions for MGPGG analysis – Statistical Tests
"""

# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd, plt, stats, np, sm
from statsmodels.stats.multicomp import pairwise_tukeyhsd
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import kruskal
import scikit_posthocs as sp


# ====================================================================================================================
# Two-Sanple t-test
# ====================================================================================================================


def gen_t_stat(sampleOne: pd.Series, sampleTwo: pd.Series):
    """_summary_

    :param sampleOne: _description_
    :param sampleTwo: _description_
    """
    t_stat, p_val = stats.ttest_ind(sampleOne, sampleTwo, equal_var=False)

    # Print the t-statistic and the p-value
    print("t-statistic:", t_stat)
    print("p-value:", p_val)

    # Interpret the p-value
    alpha = 0.05
    if p_val < alpha:
        print("Reject the null hypothesis: The means are different")
    else:
        print("Fail to reject the null hypothesis: No evidence that the means are different")

    return t_stat, p_val


# ====================================================================================================================
# Tukey mult comparison
# ====================================================================================================================


def gen_tukey_test(single_avgs: pd.Series, split_avgs: pd.Series, shared_avgs: pd.Series):
    """_summary_

    :param single_avgs: _description_
    :param split_avgs: _description_
    :param shared_avgs: _description_
    """
    data = np.concatenate([single_avgs, split_avgs, shared_avgs])
    labels = np.array(['single']*len(single_avgs) + ['split']*len(split_avgs) + ['shared']*len(shared_avgs))
    tukey = pairwise_tukeyhsd(endog=data,     # Data
                          groups=labels,  # Groups
                          alpha=0.05)     # Significance level

    # Print the result table
    print(tukey)

    # Plot the result
    tukey.plot_simultaneous()
    plt.show()


# ====================================================================================================================
# non-parametric multiple comparisons | Kruskal-Wallis ==> Conover-Iman post-hoc
# ====================================================================================================================


def gen_kruskal_wallis_and_conover_iman(single_avgs: pd.Series, split_avgs: pd.Series, shared_avgs: pd.Series):
    """_summary_

    :param single_avgs: _description_
    :param split_avgs: _description_
    :param shared_avgs: _description_
    """
    stat, p_value = kruskal(single_avgs, split_avgs, shared_avgs)

    print(f"Kruskal-Wallis H-test statistic: {stat}")
    print(f"P-value: {p_value}")

    # If p-value is significant, perform Conover-Iman posthoc test
    if p_value < 0.05:
        data = np.concatenate([single_avgs, split_avgs, shared_avgs])
        labels = ['single']*len(single_avgs) + ['split']*len(split_avgs) + ['shared']*len(shared_avgs)
        df = pd.DataFrame({'Value': data, 'Group': labels})
        
        posthoc_result = sp.posthoc_conover(df, val_col='Value', group_col='Group', p_adjust='bonferroni')
        
        print("Conover-Iman posthoc test with Bonferroni adjustment:")
        print(posthoc_result)
