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

import multiprocessing as mlt
import tqdm
import os
import numpy as np

import model
import analysis
import backup
import parameters

import argparse


def run(param):

    m = model.Model(param)
    return m.run()


def produce_data(parameters_file, data_file):

    """
    Produce data for 'pooled' condition using multiprocessing
    :param parameters_file: Path to parameters file (string)
    :param data_file: Path to the future data files (dictionary with two entries)
    :return: a 'pool backup' (arbitrary Python object)
    """

    json_parameters = parameters.load(parameters_file)

    pool_parameters = parameters.extract_parameters(json_parameters)

    pool = mlt.Pool()

    backups = []

    for bkp in tqdm.tqdm(
            pool.imap_unordered(run, pool_parameters),
            total=len(pool_parameters)):
        backups.append(bkp)

    pool_backup = backup.PoolBackup(parameters=json_parameters, backups=backups)
    pool_backup.save(parameters_file, data_file)

    return pool_backup


# def get_file_names(condition):
#
#     """
#     Give the file names depending on condition
#     :param condition: string
#     :return: Files names (tuple of size 3 containing dictionaries)
#     """
#
#     parameters_file = "parameters/json/{}.json".format(condition)
#     data_file = {
#         "pickle": "data/pickle/{}.p".format(condition),
#         "json": "data/json/{}.json".format(condition)
#     }
#
#     return parameters_file, data_file
#
#
# def get_fig_names():
#
#     folder = "data/figs"
#
#     fig_names = {
#         "distance": "{}/pool_distance.pdf".format(folder),
#         "prices_and_profits": "{}/pool_prices_and_profits.pdf".format(folder),
#         "separate": "{}/separate.pdf".format(folder),
#         "targetable_consumers": "{}/targetable_consumers.pdf".format(folder),
#         "captive_consumers": "{}/captive_consumers.pdf".format(folder)
#     }
#
#     return fig_names

# def terminal_msg(figure_files):
#
#     print("Figures produced are:")
#     for file in figure_files.values():
#         print("* '{}'".format(file))
#     print()

def data_already_produced(*args):

    """
    If data files already exist, return True
    :param args: Path to data files
    :return: True or False
    """
    return np.all([os.path.exists(i) for i in args])


def a_priori():

    """
    Produce figures for 'a priori' analysis
    :return: None
    """

    analysis.a_priori.targetable_consumers(fig_name="fig/targetable_consumers.pdf")
    analysis.a_priori.captive_consumers(
        radius=(0.25, 0.5),
        fig_name="fig/captive_consumers.pdf",
    )


def pooled_data(args):

    """
    Produce figures for 'pooled' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    for move in (str(i).replace("Move.", "") for i in (
            model.Move.max_profit, model.Move.strategic, model.Move.max_diff, model.Move.equal_sharing)):

        parameters_file = "data/json/pool_{}.json".format(move)
        data_file = "data/pickle/pool_{}.p".format(move)

        if not data_already_produced(data_file) or args.force:
            pool_backup = produce_data(parameters_file, data_file)

        else:
            pool_backup = backup.PoolBackup.load(data_file)

        analysis.pool.distance(pool_backup=pool_backup, fig_name='fig/distance_{}.pdf'.format(move))
        analysis.pool.prices_and_profits(pool_backup=pool_backup,
                                         fig_name='fig/prices_and_profits_{}.pdf'.format(move))


def individual_data(args):

    """
    Produce figures for 'individual' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    for move in (str(i).replace("Move.", "") for i in (
            model.Move.max_profit, model.Move.strategic, model.Move.max_diff, model.Move.equal_sharing)):

        run_backups = []

        for r in ("25", "50"):  # , "75"):

            parameters_file = "data/json/ind_{}_{}.json".format(r, move)
            data_file = "data/json/ind_{}_{}.json".format(r, move)

            if not data_already_produced(data_file, parameters_file) or args.force:

                json_parameters = parameters.load(parameters_file)
                param = parameters.extract_parameters(json_parameters)
                run_backup = run(param)
                run_backup.save(data_file)

            else:
                run_backup = backup.RunBackup.load(data_file)

            run_backups.append(run_backup)

        analysis.separate.separate(backups=run_backups, fig_name='fig/separate_{}.pdf'.format(move))


def main(args):

    """
    Depending on args given in command line, call the right function(s)
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    if args.new:
        args.force = True
        parameters.generate_new_parameters_files()

    if args.pooled or (not args.individual and not args.a_priori):
        pooled_data(args)

    if args.individual or (not args.pooled and not args.a_priori):
        individual_data(args)

    if args.a_priori or (not args.individual and not args.pooled):
        a_priori()

    print("Figures have been created in 'fig' folder.")
    # terminal_msg(get_fig_names())


if __name__ == "__main__":

    # Parse the arguments given in command line and call the 'main' function

    parser = argparse.ArgumentParser(description='Produce figures.')
    parser.add_argument('-f', '--force', action="store_true", default=False,
                        help="Re-run simulations")
    parser.add_argument('-n', '--new', action="store_true", default=False,
                        help="Generate new parameters files")
    parser.add_argument('-i', '--individual', action="store_true", default=False,
                        help="Do figures ONLY for individual results")
    parser.add_argument('-p', '--pooled', action="store_true", default=False,
                        help="Do figures ONLY for pooled results")
    parser.add_argument('-a', '--a_priori', action="store_true", default=False,
                        help="Do figures ONLY for a priori analysis")
    parsed_args = parser.parse_args()

    main(parsed_args)
