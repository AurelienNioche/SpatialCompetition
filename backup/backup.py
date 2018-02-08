import pickle
import json
import os


class Backup:

    def __init__(self, parameters):

        self.parameters = parameters

    def save(self, file_names):

        for i in file_names.values():
            os.makedirs(os.path.dirname(i), exist_ok=True)

        # Save a summary of parameters in json
        with open(file_names["json"], "w") as f:
            try:
                json.dump(self.parameters, f, indent=2)

            except TypeError:
                # parameters for a single run are not a dict but an arbitrary Python object
                json.dump(self.parameters.dict(), f, indent=2)

        # Save data in pickle
        with open(file_names["pickle"], "wb") as f:
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
