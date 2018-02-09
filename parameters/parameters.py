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

import json
import numpy as np


class Parameters:

    def __init__(self, r=0.5, seed=0, n_positions=20, n_prices=10, p_min=1, p_max=2, t_max=100):

        self.r = r
        self.seed = seed

        self.n_positions = n_positions
        self.n_prices = n_prices

        self.t_max = t_max

        self.p_min = p_min
        self.p_max = p_max

        self.check()

    def check(self):

        assert self.p_min < self.p_max, "'p_min' have to be inferior to 'p_max'."
        assert self.n_positions > 2, "'n_positions' have to be superior to 2."
        assert self.n_prices > 2, "'n_prices' have to be superior to 2."
        assert self.t_max > 2, "'t_max' have to be superior to 2."
        assert 0 < self.seed < 2**32-1, "'seed' have to be comprised between 0 and 2^32 - 1."
        assert 0 < self.r <= 1, "'r' have to be comprised between 0 and 1."

    def dict(self):
        return {i: j for i, j in self.__dict__.items() if not i.startswith("__")}


def load(json_file):

    with open(json_file, "r") as f:
        j_param = json.load(f)

    return j_param


def extract_parameters(j_param):

    if type(j_param["seed"]) == list:
        return [
            Parameters(
                p_min=j_param["p_min"],
                p_max=j_param["p_max"],
                n_prices=j_param["n_prices"],
                n_positions=j_param["n_positions"],
                t_max=j_param["t_max"],
                r=j_param["r"][i],
                seed=j_param["seed"][i],
            )
            for i in range(len(j_param["r"]))
        ]

    else:
        return Parameters(
                p_min=j_param["p_min"],
                p_max=j_param["p_max"],
                n_prices=j_param["n_prices"],
                n_positions=j_param["n_positions"],
                t_max=j_param["t_max"],
                r=j_param["r"],
                seed=j_param["seed"],
        )


def generate_new_parameters_files():

    n_sim = 1000
    p_min = 1
    p_max = 10
    n_prices = 50
    n_positions = 100
    t_max = 100

    for_pool = {
        "p_min": p_min,
        "p_max": p_max,
        "n_prices": n_prices,
        "n_positions": n_positions,
        "t_max": t_max,
        "seed": [int(i) for i in np.random.randint(low=0, high=2**32-1, size=n_sim)],
        "r": [float(i) for i in np.random.uniform(low=0, high=1, size=n_sim)]
    }

    with open("parameters/json/pool.json", "w") as f:
        json.dump(for_pool, f, sort_keys=True, indent=4)

    for i in (25, 50, 75):
        for_ind = {
            "p_min": p_min,
            "p_max": p_max,
            "n_prices": n_prices,
            "n_positions": n_positions,
            "t_max": t_max,
            "seed": np.random.randint(low=0, high=2**32),
            "r": i/100
        }

        with open("parameters/json/{}.json".format(i), "w") as f:
            json.dump(for_ind, f, sort_keys=True, indent=4)
