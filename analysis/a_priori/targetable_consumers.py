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

import os
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

    # Create directories if not already existing
    os.makedirs(os.path.dirname(fig_name), exist_ok=True)

    # Parameters
    seed = 123
    np.random.seed(seed)
    n_position = 210

    # Create ax
    fig = plt.figure(figsize=(3, 3), dpi=200)
    ax = fig.add_subplot(111)

    # Get data and plot it
    x = np.linspace(0, 1, n_position)

    r_values, line_styles, colors = [0.25, 0.50], ["--", "-"], ["C0", "C1"]  # , ":"]

    y = [get_targetable(r, n_position=n_position) / 10 for r in r_values]

    for i, (r, line_style, c) in enumerate(zip(r_values, line_styles, colors)):
        ax.plot(x, y[i], label="$r={:.2f}$".format(r), linewidth=1.5, clip_on=True, linestyle=line_style, color="black")
        # if i == 0:
        #     ax.fill_between(x, 0, y[i], facecolor=c, edgecolor=c, alpha=0.5)
        # else:
        #     ax.fill_between(x, y[i-1], y[i], facecolor=c, edgecolor=None, alpha=0.5)

    # Add a legend
    plt.legend()

    # Enhance aesthetics
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for tick in ax.get_xticklabels():
        tick.set_fontsize("small")
    for tick in ax.get_yticklabels():
        tick.set_fontsize("small")

    ax.set_xticks([0, 0.5, 1])
    # ax.set_yticks([25, 50, 75, 100])
    # ax.set_ylim([22, 100.3])
    ax.set_ylabel("Targetable consumers")
    ax.set_xlabel("Position")

    plt.tight_layout()

    # Save figure
    plt.savefig(fig_name)

    plt.close()
