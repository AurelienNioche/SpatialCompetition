import numpy as np
import matplotlib.pyplot as plt


def get_targetable(r, n_position):

    # Uniform position
    p = np.linspace(0, 1, n_position, endpoint=True)
    p = (np.round(p * (n_position - 1))).astype(int)

    # Same constant radius for each client
    rs = int(np.round(n_position * r)) * np.ones(n_position, dtype=int)

    # Build the local view for each client
    v = np.zeros((n_position, n_position))
    for i in range(n_position):
        lower_bound = max(0, p[i]-rs[i])
        upper_bound = min(p[i]+rs[i], n_position)
        v[i, lower_bound:upper_bound] = 1

    return v.sum(axis=0)


def targetable_consumers(fig_name):

    # Parameters
    seed = 123
    np.random.seed(seed)
    n_position = 100

    ax = plt.subplot()
    x = np.linspace(0, 1, n_position)

    for r, line_style in zip([0.25, 0.50, 0.75], ["--", "-", ":"]):
        y = get_targetable(r, n_position=n_position)
        ax.plot(x, y, label="$r={:.2f}$".format(r), linewidth=1.5, clip_on=True, linestyle=line_style, color="black")

    plt.legend()

    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    ax.set_xticks([0, 0.5, 1])
    ax.set_yticks([25, 50, 75, 100])
    ax.set_ylim([22, 100.3])
    ax.set_ylabel("Targetable consumers")
    ax.set_xlabel("Position")

    plt.savefig(fig_name)

    plt.close()
