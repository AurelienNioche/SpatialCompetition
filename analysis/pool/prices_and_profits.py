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


def prices_over_fov(pool_backup, pos_subplot):

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
    ax = plt.subplot(*pos_subplot)

    # Enhance aesthetics
    ax.set_xlim(-0.01, 1.01)

    ax.set_xticks([])
    ax.set_ylabel("Mean prices")

    # ax.set_title("Mean prices over $r$")

    # Do the hist plot
    width = boundaries[1] - boundaries[0]
    where = [np.mean((boundaries[i+1], boundaries[i])) for i in range(len(boundaries)-1)]
    ax.bar(where, height=mean_data, yerr=std_data, width=width,
           edgecolor='white', linewidth=2, facecolor="0.75")


def profits_over_fov(pool_backup, pos_subplot):

    # Shortcuts
    parameters = pool_backup.parameters
    backups = pool_backup.backups

    # Look at the parameters
    t_max = parameters["t_max"]

    # How many time steps from the end of the simulation are included in analysis
    span_ratio = 0.33  # Take last third
    span = int(span_ratio * t_max)

    # Number of bins for the barplot
    n_bins = 50

    # Compute the boundaries
    boundaries = np.linspace(0, 1, (n_bins + 1))

    # Container for data
    data = [[] for i in range(n_bins)]

    for b in backups:

        r = b.parameters.r

        for i, bound in enumerate(boundaries[1:]):
            if r <= bound:
                mean_profit = np.mean(b.profits[-span:, :])
                data[i].append(mean_profit)
                break

    mean_data = [np.mean(d) for d in data]
    std_data = [np.std(d) for d in data]

    # Create figs and plot
    ax = plt.subplot(*pos_subplot)

    # Enhance aesthetics
    ax.set_xlim(-0.01, 1.01)

    ax.set_xticks(np.arange(0, 1.1, 0.25))

    ax.set_xlabel("$r$")
    ax.set_ylabel("Mean profits")

    # ax.set_title("Mean profits over $r$")

    # Do the hist plot
    width = boundaries[1] - boundaries[0]
    where = [np.mean((boundaries[i+1], boundaries[i])) for i in range(len(boundaries)-1)]
    ax.bar(where, height=mean_data, yerr=std_data, width=width,
           edgecolor='white', linewidth=2, facecolor="0.75")


def prices_and_profits(pool_backup, fig_name):

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    plt.figure(figsize=(9, 8))

    n_rows = 2
    n_cols = 1

    prices_over_fov(pool_backup, (n_rows, n_cols, 1))

    profits_over_fov(pool_backup, (n_rows, n_cols, 2))

    # Cut margins
    plt.tight_layout()

    # Save fig
    plt.savefig(fig_name)

    plt.close()