"""
Printout in line with FGF to evaluate how serious the mistyping are 
"""


# ====================================================================================================================
# Imports
# ====================================================================================================================


from constants import pd, plt, np


# ====================================================================================================================
# Graphs
# ====================================================================================================================


def gen_sm_infographic(df: pd.DataFrame, grid_shape, figsize, conditional_columns):
    """generates infographic plot to analyze individual behavior with the strategy method conditional investment table

    :param df: mgpggdf all apps
    """
    x = [ i for i in range(0,21)]

    num_plots = df['participant.code'].nunique()
    participant_code_list = df['participant.code'].unique().tolist()

    if num_plots > np.prod(grid_shape):
        print(f"Grid shape {grid_shape} not large enough for {num_plots} plots.")
        return
    
    fig, axes = plt.subplots(*grid_shape, figsize=figsize)
    axes = axes.flatten()  # Flatten the grid of axes, so we can easily loop over them

    for i, code in enumerate(participant_code_list):
        playerType = df[df['participant.code']== code]['player.typing'].to_string()
        decisions = df[df['participant.code']== code][conditional_columns]
        y = decisions.iloc[0].tolist()
        axes[i].plot(x,y)
        axes[i].set_title(f'{code}_{playerType}', fontsize = 8)

    # Remove any unused subplots
    for i in range(num_plots, np.prod(grid_shape)):
        fig.delaxes(axes[i])

    plt.tight_layout()
    plt.show()
