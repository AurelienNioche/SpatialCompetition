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

import pickle
import json
import os


class Backup:

    def __init__(self, parameters):

        self.parameters = parameters

    def save(self, parameters_file, data_file):

        for i in (parameters_file, data_file):
            os.makedirs(os.path.dirname(i), exist_ok=True)

        # Save a summary of parameters in json
        with open(parameters_file, "w") as f:
            try:
                json.dump(self.parameters, f, indent=2)

            except TypeError:
                # parameters for a single run are not a dict but an arbitrary Python object
                json.dump(self.parameters.dict(), f, indent=2)

        # Save data in pickle
        with open(data_file, "wb") as f:
            pickle.dump(self, f)

    @staticmethod
    def load(pickle_file_name):

        with open(pickle_file_name, "rb") as f:
            return pickle.load(f)


class RunBackup(Backup):

    def __init__(self, parameters, positions, prices, profits, n_consumers):
        super().__init__(parameters)

        self.positions = positions
        self.prices = prices
        self.profits = profits
        self.n_consumers = n_consumers


class PoolBackup(Backup):

    def __init__(self, parameters, backups):
        super().__init__(parameters)

        self.backups = backups
