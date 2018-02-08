from pylab import plt, np
import os


def prices_over_fov(pool_backup, fig_name):

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    # Shortcuts
    parameters = pool_backup.parameters
    backups = pool_backup.backups

    # Look at the parameters
    t_max = parameters["t_max"]

    # Number of bins for the barplot
    n_bins = 50

    # Compute the boundaries
    boundaries = np.linspace(0, 1, (n_bins + 1))

    # How many time steps from the end of the simulation are included in analysis
    span_ratio = 0.33  # Take last third
    span = int(span_ratio * t_max)

    # Container for data
    data = [[] for i in range(n_bins)]

    for b in backups:

        r = b.parameters.r

        for i, bound in enumerate(boundaries[1:]):
            if r <= bound:
                d = np.mean(b.prices[-span:, :])
                data[i].append(d)
                break

    mean_data = [np.mean(d) for d in data]
    std_data = [np.std(d) for d in data]

    # Create figs and plot
    fig = plt.figure(figsize=(10, 4))
    ax = plt.subplot()

    # Enhance aesthetics
    ax.set_xlim(-0.01, 1.01)

    ax.set_xticks(np.arange(0, 1.1, 0.25))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean price")

    # ax.set_title("Mean prices over $r$")

    # Do the hist plot
    width = boundaries[1] - boundaries[0]
    where = [np.mean((boundaries[i+1], boundaries[i])) for i in range(len(boundaries)-1)]
    ax.bar(where, height=mean_data, yerr=std_data, width=width,
           edgecolor='white', linewidth=2, facecolor="0.75")

    # Cut the margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()
