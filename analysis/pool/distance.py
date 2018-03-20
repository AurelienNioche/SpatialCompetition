# SpatialCompetition
# Copyright (C) 2018  Aurélien Nioche, Basile Garcia & Nicolas Rougier
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from pylab import plt, np
import os


def distance(pool_backup, fig_name, color=False):

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
    z = np.zeros(n_simulations)
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

        y[i] = spacing

        # Get std
        y_err[i] = np.std(data)

        # Get mean profits
        z[i] = np.mean(b.profits[-span:, :])

    # Plot this
    fig = plt.figure(figsize=(5, 5), dpi=200)
    ax = plt.subplot()

    # Enhance aesthetics
    ax.set_xlim(-0.009, 1.005)
    ax.set_ylim(-0.009, 1.005)
    # if max(y) < 0.5:
    #     ax.set_ylim(-0.01, 0.51)

    ax.set_xticks(np.arange(0, 1.1, 0.25))
    ax.set_yticks(np.arange(0, 1.1, 0.25))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Distance")

    # ax.set_title("Mean distance between firms over $r$")

    # Display line for indicating 'random' level
    # seed = 123
    # np.random.seed(seed)
    # random_pos = np.random.random(size=(2, 10 ** 6))
    # random_dist = np.mean(np.absolute(random_pos[0] - random_pos[1]))
    # ax.axhline(random_dist, color='0.5', linewidth=0.5, linestyle="--", zorder=1)

    if color:
        _color(fig=fig, ax=ax, x=x, y=y, z=z)
    else:
        _bw(ax=ax, x=x, y=y, y_err=y_err)

    # Cut the margins
    plt.tight_layout()

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)
    # Save fig
    plt.savefig(fig_name)

    plt.close()


def _bw(ax, x, y, y_err):

    # Do the scatter plot
    ax.scatter(x, y, facecolor="black", edgecolor='white', s=15, alpha=1)

    # Error bars
    ax.errorbar(x, y, yerr=y_err, fmt='.', color="0.80", zorder=-10, linewidth=0.5)


def _color(fig, ax, x, y, z):

    # Do the scatter plot
    scat = ax.scatter(x, y, c=z, zorder=10, alpha=0.25)

    # Add a color bar
    fig.colorbar(scat, label="Profits")
