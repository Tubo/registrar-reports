import re
import sys, argparse, pathlib
import pandas as pd
import numpy as np

from src.parts_parser import parse as parse_bodyparts


def parse_ris(args):
    inputname = args.input
    outname = "output/ris_count/ExamDataParsed_.csv"

    data = pd.read_csv(inputname)
    parts_sum = data["ce_description"].apply(parse_bodyparts)
    parsed = pd.concat([data, parts_sum.rename("parts_sum")], axis=1)
    result = pd.concat([data, parsed.parts_sum.rename("parts_sum")], axis=1)
    result.to_csv(outname)


def crawl_impressions(args):
    print("crawling")


parser = argparse.ArgumentParser(prog="Registrar Reporting Numbers Utility")
subparsers = parser.add_subparsers(
    title="subcommands", required=True, help="Parse body parts or Crawl impression?"
)

parser_a = subparsers.add_parser("parse")
parser_a.set_defaults(func=parse_ris)
parser_a.add_argument("--input")

parser_b = subparsers.add_parser("crawl")
parser_b.set_defaults(func=crawl_impressions)
parser_b.add_argument("--start")
parser_b.add_argument("--finish")
parser_b.add_argument("--names")

args = parser.parse_args()

args.func(args)


""" filename = sys.argv[1]

"""
