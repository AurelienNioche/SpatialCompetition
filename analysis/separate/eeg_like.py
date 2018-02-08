import numpy as np
import matplotlib.pyplot as plt
import os


def eeg_like(backup, fig_name):

    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    pst = backup.positions
    prc = backup.prices

    t_max = backup.parameters.t_max

    t = np.arange(1, t_max)

    position_max = backup.parameters.n_positions - 1

    position_A = pst[1:t_max, 0] / position_max
    position_B = pst[1:t_max, 1] / position_max
    price_A = prc[1:t_max, 0]
    price_B = prc[1:t_max, 1]

    color_A = "orange"
    color_B = "blue"

    price_min = backup.parameters.p_min
    price_max = backup.parameters.p_max

    fig = plt.Figure()

    # Position firm A

    ax = plt.subplot(4, 1, 1)
    ax.plot(t, position_A, color=color_A, alpha=1, linewidth=1.1)
    ax.plot(t, np.ones(len(t)) * 0.5, color='0.5', linewidth=0.5, linestyle='dashed', zorder=-10)
    # ax.plot(t, position_B, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([0, 1])
    ax.set_ylabel('Position $a$', labelpad=16)

    # Add title
    plt.title("Evolution of positions and prices ($r={}$)".format(backup.parameters.r))

    # Position firm B

    ax = plt.subplot(4, 1, 2)
    ax.plot(t, position_B, color=color_B, alpha=1, linewidth=1.1)
    ax.plot(t, np.ones(len(t)) * 0.5, color='0.5', linewidth=0.5, linestyle='dashed', zorder=-10)
    # ax.plot(t, position_A, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([0, 1])
    ax.set_ylabel('Position $b$', labelpad=16)

    # Price firm A

    ax = plt.subplot(4, 1, 3)
    ax.plot(t, price_A, color=color_A, alpha=1, linewidth=1.1, clip_on=False)
    # ax.plot(t, price_B, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price $a$', labelpad=10)  # , rotation=0)
    ax.set_ylim([price_min, price_max])

    # Price firm B

    ax = plt.subplot(4, 1, 4)
    ax.plot(t, price_B, color=color_B, alpha=1, linewidth=1.1, clip_on=False)
    # ax.plot(t, price_A, color="black", alpha=0.5, linewidth=1)
    ax.spines['top'].set_color('none')
    ax.spines['right'].set_color('none')
    ax.spines['bottom'].set_color('none')
    ax.set_xticks([])
    ax.set_yticks([price_min, price_max])
    ax.set_ylabel('Price $b$', labelpad=10)  # , rotation=0)
    ax.set_ylim([price_min, price_max])

    ax.set_xlabel("Time", labelpad=10)

    # Cut margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()

