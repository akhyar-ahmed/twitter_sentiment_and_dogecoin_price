
import argparse
import logging
from datetime import datetime
import os
import random
import torch
import numpy as np
import sys


def read_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--dataset_path", default="data", type=str)
    parser.add_argument("--scraper", default="twint", type=str)
    parser.add_argument("--scraper_limit", default=10, type=int)
    parser.add_argument("--dataset", type=str)
    parser.add_argument("--log_folder", type=str, default="logs")
    parser.add_argument("--experiment_name", type=str, default="")
    parser.add_argument("--asset_path", type=str, default="assets")
    parser.add_argument("--output_dir", type=str, default="datasets")
    parser.add_argument("--logging_steps", type=int, default=100)
    parser.add_argument("--subsample", type=int, default=-1)
    parser.add_argument("--device", default=0, type=int, help="GPU device #")
    parser.add_argument("--local_rank", default=-1, type=int)
    return parser.parse_args()


# create the output folder
def make_log_folder(args, name):
    if not os.path.exists(args.log_folder):
        os.mkdir(args.log_folder)

    my_date = datetime.now()

    folder_name=my_date.strftime('%Y-%m-%dT%H-%M-%S') + "_" + name

    if len(args.experiment_name) > 0:
        folder_name += "_" + args.experiment_name

    log_folder=os.path.join(args.log_folder, folder_name)
    os.mkdir(log_folder)
    return log_folder


# log to file and console
def create_logger(log_dir):
    logFormatter = logging.Formatter("%(asctime)s [%(levelname)s] {%(filename)s:%(lineno)d} %(message)s")
    rootLogger = logging.getLogger()

    fileHandler = logging.FileHandler(os.path.join(log_dir, "log.txt"))
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)

    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)

    rootLogger.setLevel(logging.INFO)



def init_experiments(args, experiment_name):
    log_dir=make_log_folder(args, experiment_name)
    logging.info(log_dir)
    create_logger(log_dir)

    command=" ".join(sys.argv)
    logging.info('''Twitter Sentiment with Dogecoin ''')
    logging.info("start command: " + command)
    logging.info(f"experiment name {experiment_name}")
    logging.info(args)
    return log_dir

