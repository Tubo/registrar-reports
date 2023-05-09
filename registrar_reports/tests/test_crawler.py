import os
from pyquery import PyQuery as pq

from ..src.impression_crawler import *


class TestTableParser:
    def test_table_parse(self):
        with open("registrar_reports/tests/table.html") as f:
            page = f.read()

        table = parse_table(page)
        assert len(table) == 27
