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
    pool_backup.save(data_file)

    return pool_backup


def get_file_names(condition):

    """
    Give the file names depending on condition
    :param condition: string
    :return: Files names (tuple of size 3 containing dictionaries)
    """

    parameters_file = "parameters/json/{}.json".format(condition)
    data_file = {
        "pickle": "data/pickle/{}.p".format(condition),
        "json": "data/json/{}.json".format(condition)
    }

    return parameters_file, data_file


def get_fig_names():

    folder = "data/figs"

    fig_names = {
        "distance": "{}/pool_distance.pdf".format(folder),
        "prices_and_profits": "{}/pool_prices_and_profits.pdf".format(folder),
        "separate": "{}/separate.pdf".format(folder),
        "targetable_consumers": "{}/targetable_consumers.pdf".format(folder),
        "captive_consumers": "{}/captive_consumers.pdf".format(folder)
    }

    return fig_names


def data_already_produced(data_file):

    """
    If data files already exist, return True
    :param data_file: Path to data file (dictionary with two entries)
    :return: True or False
    """
    return os.path.exists(data_file["json"]) and os.path.exists(data_file["pickle"])


def terminal_msg(figure_files):

    print("Figures produced are:")
    for file in figure_files.values():
        print("* '{}'".format(file))
    print()


def a_priori():

    """
    Produce figures for 'a priori' analysis
    :return: None
    """

    figure_names = get_fig_names()
    radius = (0.25, 0.5, 0.75)

    analysis.a_priori.targetable_consumers(figure_names["targetable_consumers"])
    analysis.a_priori.captive_consumers(
        radius=radius,
        fig_name=figure_names["captive_consumers"],
    )


def pooled_data(args):

    """
    Produce figures for 'pooled' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    condition = "pool"

    parameters_file, data_file = get_file_names(condition)
    fig_names = get_fig_names()

    if not data_already_produced(data_file) or args.force:
        pool_backup = produce_data(parameters_file, data_file)

    else:
        pool_backup = backup.PoolBackup.load(data_file["pickle"])

    analysis.pool.distance(pool_backup=pool_backup, fig_name=fig_names["distance"])
    analysis.pool.prices_and_profits(pool_backup=pool_backup, fig_name=fig_names["prices_and_profits"])


def individual_data(args):

    """
    Produce figures for 'individual' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    run_backups = []

    for condition in ("25", "50", "75"):

        parameters_file, data_file = get_file_names(condition)

        if not data_already_produced(data_file) or args.force:

            json_parameters = parameters.load(parameters_file)
            param = parameters.extract_parameters(json_parameters)
            run_backup = run(param)
            run_backup.save(data_file)

        else:
            run_backup = backup.RunBackup.load(data_file["pickle"])

        run_backups.append(run_backup)

    analysis.separate.separate(backups=run_backups, fig_name=get_fig_names()["separate"])


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

    terminal_msg(get_fig_names())


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
