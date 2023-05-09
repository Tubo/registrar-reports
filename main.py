import re
from datetime import datetime
import sys, argparse, pathlib, os
import pandas as pd
import numpy as np
from dotenv import dotenv_values

from registrar_reports import *


def parse_ris(args):
    inputname = args.input
    output_suffix = input("What is the date range of the parsed data: ")
    outname = f"output/ris_count/ExamDataParsed_{output_suffix}.csv"

    data = pd.read_csv(inputname)
    data.dropna(how="all", inplace=True)  # remove empty rows
    parts_sum = data["ce_description"].apply(parse_bodyparts)
    parsed = pd.concat([data, parts_sum.rename("parts_sum")], axis=1)
    result = pd.concat([data, parsed.parts_sum.rename("parts_sum")], axis=1)
    result.to_csv(outname)


def crawl_impressions(args):
    users = pd.read_excel("Impressions.xlsx")
    config = dotenv_values()
    output_fn = datetime.now().strftime("%Y-%m-%dT%H%M%S")
    output = f"output/impression_count/{output_fn}.txt"

    df = IVCrawler(config, users).start()
    # df.to_pickle(f"notebooks/{output_fn}.pkl")
    summary = df.groupby("user").modality.value_counts()
    pd.DataFrame(summary).to_string(output)


parser = argparse.ArgumentParser(prog="Registrar Reporting Numbers Utility")
subparsers = parser.add_subparsers(
    title="subcommands", required=True, help="Parse body parts or Crawl impression?"
)

parser_a = subparsers.add_parser("parse")
parser_a.set_defaults(func=parse_ris)
parser_a.add_argument("-f")

parser_b = subparsers.add_parser("crawl")
parser_b.set_defaults(func=crawl_impressions)

args = parser.parse_args()

args.func(args)
