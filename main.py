import argparse
import os
import pathlib
import re
import sys
from datetime import datetime
import getpass

import numpy as np
import pandas as pd
from dotenv import dotenv_values

from registrar_reports import *


def parse_ris(args):
    inputname = args.input
    output_suffix = input(
        "To help name the output file, what is the date range of the parsed data (YYYYMMDD-YYYMMDD):\n"
    )
    outname = f"output/ris_count/ExamDataParsed_{output_suffix}.csv"

    data = pd.read_csv(inputname)
    data.dropna(how="all", inplace=True)  # remove empty rows
    parts_sum = data["ce_description"].apply(parse_bodyparts)
    parsed = pd.concat([data, parts_sum.rename("parts_sum")], axis=1)
    result = pd.concat([data, parsed.parts_sum.rename("parts_sum")], axis=1)
    result.to_csv(outname)


def get_credentials(config):
    """Get credentials from config or prompt user if empty"""
    credentials = {}
    field_prompts = {
        "LOGIN": "Inteleviewer Username",
        "IVPW": "Inteleviewer Password",
        "CDHBPW": "Single Sign-On Password",
        "IB_URL": "InteleBrowser URL"
    }
    
    for field, prompt in field_prompts.items():
        if field not in config or not config[field]:
            if field in ["IVPW", "CDHBPW"]:
                # Use getpass for passwords to hide input
                credentials[field] = getpass.getpass(f"Please enter your {prompt}: ")
            else:
                credentials[field] = input(f"Please enter your {prompt}: ")
        else:
            credentials[field] = config[field]
    
    return credentials


def crawl_impressions(args):
    users = pd.read_excel("Impressions.xlsx")
    config = dotenv_values()
    credentials = get_credentials(config)
    
    output_dir = "output/impression_count/"
    raw_file = output_dir + "raw.csv"
    output_fn = output_dir + f"{datetime.now().strftime("%Y-%m-%dT%H%M%S")}.csv"

    df = InteleBrowserCrawler(credentials, users).run()
    df.to_csv(raw_file)
    df = pd.read_csv(raw_file)
    result = analyse(df)
    result.to_csv(output_fn)


parser = argparse.ArgumentParser(prog="Registrar Reporting Numbers Utility")
subparsers = parser.add_subparsers(
    title="subcommands", required=True, help="Parse body parts or Crawl impression?"
)

parser_a = subparsers.add_parser("parse")
parser_a.set_defaults(func=parse_ris)
parser_a.add_argument("-f", dest="input")

parser_b = subparsers.add_parser("crawl")
parser_b.set_defaults(func=crawl_impressions)

args = parser.parse_args()

args.func(args)
