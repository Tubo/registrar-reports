import re
import sys
import pandas as pd
import numpy as np

from descriptor_parser.src.parser import parse

filename = sys.argv[1]
outname = "descriptor_parser/output/ExamDataParsed_.csv"

data = pd.read_csv(filename)
parts_sum = data["ce_description"].apply(parse)
parsed = pd.concat([data, parts_sum.rename("parts_sum")], axis=1)
result = pd.concat([data, parsed.parts_sum.rename("parts_sum")], axis=1)
result.to_csv(outname)
