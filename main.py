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
import matplotlib.pyplot as plt
import matplotlib.gridspec

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

        # analysis.pool.distance(pool_backup=pool_backup, fig_name='fig/distance_{}.pdf'.format(move))
        # analysis.pool.prices_and_profits(pool_backup=pool_backup,
        #                                  fig_name='fig/prices_and_profits_{}.pdf'.format(move))
        analysis.pool.distance_price_and_profit(pool_backup=pool_backup,
                                                fig_name="fig/distance_price_profit_{}.pdf".format(move))


def batch_data(args):

    """
    Produce figures for 'pooled' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    for move in (str(i).replace("Move.", "") for i in (
            model.Move.max_profit, model.Move.strategic, model.Move.max_diff, model.Move.equal_sharing)):

        parameters_file = "data/json/batch_{}.json".format(move)
        data_file = "data/pickle/batch_{}.p".format(move)

        if not data_already_produced(data_file) or args.force:
            batch_backup = produce_data(parameters_file, data_file)

        else:
            batch_backup = backup.PoolBackup.load(data_file)

        analysis.batch.plot(batch_backup=batch_backup, fig_name='fig/batch_{}.pdf'.format(move))


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

            parameters_file = "data/json/{}_{}.json".format(r, move)
            data_file = "data/pickle/{}_{}.p".format(r, move)

            if not data_already_produced(parameters_file, data_file) or args.force:

                json_parameters = parameters.load(parameters_file)
                param = parameters.extract_parameters(json_parameters)
                run_backup = run(param)
                run_backup.save(parameters_file, data_file)

            else:
                run_backup = backup.RunBackup.load(data_file)

            run_backups.append(run_backup)

        analysis.separate.separate(backups=run_backups, fig_name='fig/separate_{}.pdf'.format(move))


def clustered_data(args):

    for move in (str(i).replace("Move.", "") for i in (
            model.Move.max_profit, model.Move.strategic, model.Move.max_diff, model.Move.equal_sharing)):

        parameters_file = "data/json/pool_{}.json".format(move)
        data_file = "data/pickle/pool_{}.p".format(move)

        if not data_already_produced(data_file) or args.force:
            pool_backup = produce_data(parameters_file, data_file)

        else:
            pool_backup = backup.PoolBackup.load(data_file)

        run_backups = []

        for r in ("25", "50"):  # , "75"):

            parameters_file = "data/json/{}_{}.json".format(r, move)
            data_file = "data/pickle/{}_{}.p".format(r, move)

            if not data_already_produced(parameters_file, data_file) or args.force:

                json_parameters = parameters.load(parameters_file)
                param = parameters.extract_parameters(json_parameters)
                run_backup = run(param)
                run_backup.save(parameters_file, data_file)

            else:
                run_backup = backup.RunBackup.load(data_file)

            run_backups.append(run_backup)

        parameters_file = "data/json/batch_{}.json".format(move)
        data_file = "data/pickle/batch_{}.p".format(move)

        if not data_already_produced(data_file) or args.force:
            batch_backup = produce_data(parameters_file, data_file)

        else:
            batch_backup = backup.PoolBackup.load(data_file)

        fig = plt.figure(figsize=(13.5, 7))
        gs = matplotlib.gridspec.GridSpec(nrows=2, ncols=2, width_ratios=[1, 0.7])

        analysis.pool.distance_price_and_profit(pool_backup=pool_backup, subplot_spec=gs[0, 0])
        analysis.separate.separate(backups=run_backups, subplot_spec=gs[:, 1])
        analysis.batch.plot(batch_backup=batch_backup, subplot_spec=gs[1, 0])

        plt.tight_layout()

        ax = fig.add_subplot(gs[:, :], zorder=-10)

        plt.axis("off")
        ax.text(
            s="B", x=-0.05, y=0, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
            fontsize=20)
        ax.text(
            s="A", x=-0.05, y=0.55, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
            fontsize=20)
        ax.text(
            s="C", x=0.58, y=0, horizontalalignment='center', verticalalignment='center', transform=ax.transAxes,
            fontsize=20)

        fig_name = "fig/clustered_{}.pdf".format(move)
        os.makedirs(os.path.dirname(fig_name), exist_ok=True)
        plt.savefig(fig_name)
        plt.show()


def main(args):

    """
    Depending on args given in command line, call the right function(s)
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    if args.new:
        args.force = True
        parameters.generate_new_parameters_files()

    if args.pooled:
        pooled_data(args)

    if args.individual:
        individual_data(args)

    if args.batch:
        batch_data(args)

    if args.a_priori:
        a_priori()

    if (not args.pooled and not args.individual and not args.batch and not args.a_priori) or args.clustered:
        clustered_data(args)

    print("Figures have been created in 'fig' folder.")


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
    parser.add_argument('-b', '--batch', action="store_true", default=False,
                        help="Do figures ONLY for batch analysis (2 values of r)")
    parser.add_argument('-c', '--clustered', action="store_true", default=False,
                        help="Do figures in a 'clustered' mode")
    parsed_args = parser.parse_args()

    main(parsed_args)
