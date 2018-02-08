import os
from pylab import plt


def pos_firmA_over_pos_firmB(backup, fig_name):

    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    position_max = backup.parameters.n_positions - 1

    pos = backup.positions[-1000:] / position_max

    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.scatter(pos[:, 0], pos[:, 1], color="black", alpha=0.05, zorder=10)
    ax.axvline(0.5, color="0.5", linewidth=0.5, linestyle="--", zorder=1)
    ax.axhline(0.5, color="0.5", linewidth=0.5, linestyle="--", zorder=1)

    plt.xlim(0, 1)
    plt.ylim(0, 1)
    plt.xticks((0, 0.5, 1))
    plt.yticks((0, 0.5, 1))

    plt.xlabel("Position $a$")
    plt.ylabel("Position $b$")

    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    plt.title("$r={:.2f}$".format(backup.parameters.r))
    ax.set_aspect(1)

    # Cut margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()
