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


def get_files_names(condition):

    """
    Give the files names depending on condition
    :param condition: string
    :return: Files names (tuple of size 3 containing dictionaries)
    """

    parameters_file = "parameters/json/{}.json".format(condition)
    data_file = {
        "pickle": "data/pickle/{}.p".format(condition),
        "json": "data/json/{}.json".format(condition)
    }

    if condition == 'pool':
        fig_names = {
            "distance": "data/figs/{}_distance.pdf".format(condition),
            "prices": "data/figs/{}_prices.pdf".format(condition),
            "profits": "data/figs/{}_profits.pdf".format(condition)
        }

    else:
        fig_names = {
            "eeg_like": "data/figs/eeg_like_{}.pdf".format(condition),
            "positions": "data/figs/positions_{}.pdf".format(condition)
        }

    return parameters_file, data_file, fig_names


def data_already_produced(data_file):

    """
    If data files already exist, return True
    :param data_file: Path to data file (dictionary with two entries)
    :return: True or False
    """
    return os.path.exists(data_file["json"]) and os.path.exists(data_file["pickle"])


def terminal_msg(condition, parameters_file, data_file, figure_files):

    """
    :param condition: Name of condition (string)
    :param parameters_file: Path to parameters file (string)
    :param data_file: Path to data file (dictionary with two entries)
    :param figure_files: Path to figure files (dictionary with n entries)
    :return: None
    """

    print("\n************ For '{}' results **************".format(condition))
    print()
    print("Parameters file used is: '{}'\n".format(parameters_file))
    print("Data files are:\n"
          "* '{}' for parameters\n"
          "* '{}' for data itself\n".format(parameters_file, data_file["json"], data_file["pickle"]))
    print("Figures files are:")
    for file in figure_files.values():
        print("* '{}'".format(file))
    print()


def a_priori():

    """
    Produce figures for 'a priori' analysis
    :return: None
    """

    figure_files = {
        "targetable_consumers": "data/figs/targetable_consumers.pdf",
        "captive_consumers": "data/figs/captive_consumers.pdf"
    }

    analysis.a_priori.targetable_consumers(figure_files["targetable_consumers"])
    analysis.a_priori.captive_consumers_inline_figures(
        radius=(0.25, 0.5, 0.75),
        fig_name=figure_files["captive_consumers"],
    )

    print("\n************ For 'a priori' analysis **************\n")
    print("Figures files are:")
    for file in figure_files.values():
        print("* '{}'".format(file))
    print()


def pooled_data(args):

    """
    Produce figures for 'pooled' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    condition = "pool"

    parameters_file, data_file, fig_files = get_files_names(condition)

    if not data_already_produced(data_file) or args.force:
        pool_backup = produce_data(parameters_file, data_file)

    else:
        pool_backup = backup.PoolBackup.load(data_file["pickle"])

    analysis.pool.distance_over_fov(pool_backup=pool_backup, fig_name=fig_files["distance"])
    analysis.pool.prices_over_fov(pool_backup=pool_backup, fig_name=fig_files["prices"])
    analysis.pool.profits_over_fov(pool_backup=pool_backup, fig_name=fig_files["profits"])

    terminal_msg(condition, parameters_file, data_file, fig_files)


def individual_data(args):

    """
    Produce figures for 'individual' data
    :param args: Parsed args from command line ('Namespace' object)
    :return: None
    """

    for condition in ("75", "50", "25"):

        parameters_file, data_file, fig_files = get_files_names(condition)

        if not data_already_produced(data_file) or args.force:

            json_parameters = parameters.load(parameters_file)
            param = parameters.extract_parameters(json_parameters)
            run_backup = run(param)
            run_backup.save(data_file)

        else:
            run_backup = backup.RunBackup.load(data_file["pickle"])

        analysis.separate.eeg_like(backup=run_backup, fig_name=fig_files["eeg_like"])
        analysis.separate.pos_firmA_over_pos_firmB(backup=run_backup, fig_name=fig_files["positions"])

        terminal_msg(condition, parameters_file, data_file, fig_files)


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


if __name__ == "__main__":

    """
    Parse the arguments given in command line and call the 'main' function
    """

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
