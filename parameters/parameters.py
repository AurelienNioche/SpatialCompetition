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
import json
import numpy as np

from model import model


class Parameters:

    def __init__(self, r=0.5, seed=0, n_positions=20, n_prices=10, p_min=1, p_max=2, t_max=25,
                 move=model.Move.max_profit):

        self.r = r
        self.seed = seed

        self.n_positions = n_positions
        self.n_prices = n_prices

        self.t_max = t_max

        self.p_min = p_min
        self.p_max = p_max

        self.move = move

        self.check()

    def check(self):

        assert self.p_min < self.p_max, "'p_min' have to be inferior to 'p_max'."
        assert self.n_positions > 2, "'n_positions' have to be superior to 2."
        assert self.n_prices > 2, "'n_prices' have to be superior to 2."
        assert self.t_max > 2, "'t_max' have to be superior to 2."
        assert 0 < self.seed < 2**32-1, "'seed' have to be comprised between 0 and 2^32 - 1."
        assert 0 < self.r <= 1, "'r' have to be comprised between 0 and 1."

    def dict(self):
        dic = {i: j for i, j in self.__dict__.items() if not i.startswith("__")}
        dic["move"] = str(dic["move"]).replace("Move.", "")
        return dic


def load(json_file):

    if not os.path.exists(json_file):
        generate_new_parameters_files()

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
                move=getattr(model.Move, j_param["move"])
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
                move=getattr(model.Move, j_param["move"])
        )


def generate_new_parameters_files():

    n_pool = 1000
    n_batch = 50

    p_min = 1
    p_max = 11
    n_prices = 11
    n_positions = 21
    t_max = 25

    to_create = []

    for move in (
        model.Move.max_profit, model.Move.strategic, model.Move.max_diff,
        model.Move.equal_sharing
    ):
        str_move = str(move).replace("Move.", "")

        # ------ Pool ---------- #

        for_pool = {
            "p_min": p_min,
            "p_max": p_max,
            "n_prices": n_prices,
            "n_positions": n_positions,
            "t_max": t_max,
            "seed": [int(i) for i in np.random.randint(low=0, high=2**32-1, size=n_pool)],
            "r": [float(i) for i in np.random.uniform(low=0, high=1, size=n_pool)],
            "move": str_move,
        }

        to_create.append(("data/json/pool_{}.json".format(str_move), for_pool))

        # ------ Batch --------- #

        assert n_batch % 2 == 0, "Number of batch should be a pair number"

        for_batch = {
            "p_min": p_min,
            "p_max": p_max,
            "n_prices": n_prices,
            "n_positions": n_positions,
            "t_max": t_max,
            "seed": [int(i) for i in np.random.randint(low=0, high=2**32-1, size=n_batch)],
            "r": [0.25, ] * (n_batch//2) + [0.50, ] * (n_batch//2),
            "move": str_move,
        }

        to_create.append(("data/json/batch_{}.json".format(str_move), for_batch))

        # ---- Separate -------- #

        for i in (25, 50):
            for_ind = {
                "p_min": p_min,
                "p_max": p_max,
                "n_prices": n_prices,
                "n_positions": n_positions,
                "t_max": t_max,
                "seed": np.random.randint(low=0, high=2**32),
                "r": i/100,
                "move": str_move
            }

            to_create.append(("data/json/{}_{}.json".format(i, str_move), for_ind))

    for f_name, content in to_create:
        with open(f_name, "w") as f:
            json.dump(content, f, sort_keys=True, indent=4)
