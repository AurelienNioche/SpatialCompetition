from pylab import plt, np
import os


def distance_over_fov_bw(pool_backup, fig_name):

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    # Shortcuts
    parameters = pool_backup.parameters
    backups = pool_backup.backups

    # Look at the parameters
    n_simulations = len(parameters["seed"])
    n_positions = parameters["n_positions"]
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

        # Compute the mean distance between the two firms
        data = np.absolute(
            b.positions[-span:, 0] -
            b.positions[-span:, 1]) / n_positions

        spacing = np.mean(data)
        spacing_std = np.std(data)

        y[i] = spacing
        y_err[i] = spacing_std

        # Get mean profits
        z[i] = np.mean(b.profits[-span:, :])

    # Create fig and axes
    fig = plt.figure(figsize=(10, 6))
    ax = plt.subplot()

    # Enhance aesthetics
    ax.set_xlim(-0.01, 1.01)
    if max(y) < 0.5:
        ax.set_ylim(-0.01, 0.51)

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    ax.set_yticks(np.arange(0, 0.51, 0.1))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean distance")

    ax.set_title("Mean distance between firms over $r$")

    # Display line for indicating 'random' level
    seed = 123
    np.random.seed(seed)
    random_pos = np.random.random(size=(2, 10 ** 6))
    random_dist = np.mean(np.absolute(random_pos[0] - random_pos[1]))
    ax.axhline(random_dist, color='0.5', linewidth=0.5, linestyle="--", zorder=1)

    # Do the scatter plot
    ax.scatter(x, y, facecolor="black", edgecolor='none', s=25, alpha=0.15)

    # Error bars
    ax.errorbar(x, y, yerr=y_err, fmt='.', alpha=0.1)

    # Cut the margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()


