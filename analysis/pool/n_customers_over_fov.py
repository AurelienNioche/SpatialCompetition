from pylab import plt, np
import os


def prices_over_fov(pool_backup, fig_name):

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    # Shortcuts
    parameters = pool_backup.parameters
    backups = pool_backup.backups

    # Look at the parameters
    n_simulations = len(parameters["seed"])
    t_max = parameters["t_max"]

    # Containers
    x = np.zeros(n_simulations)
    y = np.zeros(n_simulations)
    y_err = np.zeros(n_simulations)

    # How many time steps from the end of the simulation are included in analysis
    span_ratio = 0.33  # Take last third
    span = int(span_ratio * t_max)

    for i, b in enumerate(backups):
        x[i] = b.parameters.r

        data = np.mean(b.n_customers[-span:, :])
        data_std = np.std(data)

        y[i] = data
        y_err[i] = data_std

    # Create figs and plot
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    # Enhance aesthetics
    ax.set_xlim(-0.01, 1.01)
    # ax.set_ylim(-0.01, max(y))

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    # ax.set_yticks(np.arange(0, 0.51, 0.1))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean number of consumers")

    ax.set_title("Mean prices over $r$")

    # Do the scatter plot
    ax.scatter(x, y, facecolor="black", edgecolor='none', s=25, alpha=0.15)

    # Error bars
    ax.errorbar(x, y, yerr=y_err, fmt='.', alpha=0.1)

    # Cut the margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()
