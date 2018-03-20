import os
import matplotlib.pyplot as plt
import matplotlib.gridspec

from . distance import distance
from . prices_and_profits import prices_and_profits


def distance_price_and_profit(pool_backup, fig_name=None, subplot_spec=None):

    nrows, ncols = 1, 2

    if subplot_spec is None:

        fig = plt.figure(figsize=(10, 5), dpi=200)
        gs = matplotlib.gridspec.GridSpec(nrows=nrows, ncols=ncols)

    else:
        gs = matplotlib.gridspec.GridSpecFromSubplotSpec(
            nrows=nrows, ncols=ncols, subplot_spec=subplot_spec, wspace=0.3)

    ax_distance = plt.subplot(gs[0, 0])

    gs2 = matplotlib.gridspec.GridSpecFromSubplotSpec(subplot_spec=gs[0, 1], nrows=2, ncols=1)
    ax_price = plt.subplot(gs2[0, 0])
    ax_profit = plt.subplot(gs2[1, 0])

    distance(pool_backup=pool_backup, ax=ax_distance)
    prices_and_profits(pool_backup=pool_backup, ax_price=ax_price, ax_profit=ax_profit)

    if fig_name:

        # Cut margins
        plt.tight_layout()

        # Create directories if not already existing
        os.makedirs(os.path.dirname(fig_name), exist_ok=True)

        # Save fig
        plt.savefig(fig_name)

        plt.close()
