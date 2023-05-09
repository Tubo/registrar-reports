import time
from datetime import datetime
import os, pathlib

import requests
import pandas as pd
from pandas import DataFrame
from pyquery import PyQuery as pq


class IVCrawler:
    FRAME_TIMEOUT = 2 * 60 * 1000

    def __init__(self, config, users) -> None:
        # base64 decode
        self.username = config["LOGIN"]
        self.password = config["IVPW"]
        self.cdhb_pass = config["CDHBPW"]
        self.base_url = config["IB_URL"]
        self.users = users.dropna()
        self.is_logged_in = False

    def start(self) -> None:
        with requests.Session() as s:
            s.auth = (self.username, self.cdhb_pass)
            self.session = s

            self.log_in()

            result = []
            for _, user in self.users.iterrows():
                data = self.fetch_user_data(user.Username, user.Start, user.End)
                result.extend(data)

            assert result, "Empty result, something went wrong"
            return DataFrame(result)

    def fetch_user_data(self, username, start, end) -> list:
        # Direct POST request
        # todo: parsing results with bs4
        if not self.is_logged_in:
            assert False, "Not logged in"

        start = start.strftime("%Y/%m/%d")
        end = end.strftime("%Y/%m/%d")

        if cache := self.retrieve_cache(username, start, end):
            return cache

        response = self.session.post(
            f"{self.base_url}/app",
            data={
                "service": "direct/1/AuditDetails/$Form",
                "sp": "S0",
                "Form0": "usernameFilter,$PropertySelection,patientIdFilter,studyDescriptionFilter,$PropertySelection$0,$Checkbox,$Checkbox$0,$Checkbox$1,$Checkbox$2,$Checkbox$3,$Checkbox$4,$Checkbox$5,$Checkbox$6,$Checkbox$7,$Checkbox$8,$Checkbox$9,$Checkbox$10,$Checkbox$11,$Checkbox$12,$Checkbox$13,$Checkbox$14,$Checkbox$15,$Checkbox$16,$Checkbox$17,$Checkbox$18,$Checkbox$19,$Checkbox$20,$Checkbox$21,$Checkbox$22,$Checkbox$23,$Checkbox$24,$Checkbox$25,$Checkbox$26,$Checkbox$27,$Checkbox$28,$Checkbox$29,$Checkbox$30,$Checkbox$31,$Checkbox$32,$Checkbox$33,$Checkbox$34,$Checkbox$35,$Checkbox$36,$Checkbox$37,$Checkbox$38,$Checkbox$39,$Checkbox$40,$Checkbox$41,$Submit",
                "usernameFilter": username,
                "$PropertySelection": "anyRole",
                "patientIdFilter": "",
                "studyDescriptionFilter": "",
                "$PropertySelection$0": f"{start}:{end}",
                "$Checkbox$2": "on",
                "$Submit": "Update",
            },
        )
        result = [response.content]

        while has_next_page(response.content):
            response = self.session.get(
                f"{self.base_url}/app?service=direct/1/AuditDetails/auditDetailsTable.customPaginationControlTop.nextPage"
            )
            result.append(response.content)

        result = parse_pages(result)
        self.save_cache(result)
        return result

    def save_cache(self, result):
        # todo
        pass

    def retrieve_cache(self, username, start, end):
        # todo: implement cache
        return False

    def log_in(self):
        resp = self.session.post(
            f"{self.base_url}/login/ws/auth",
            data={
                "username": "TuboS",
                "password": "Imadoctor12",
                "mfaToken": "",
                "keepMeLoggedIn": "false",
            },
        )

        if resp.status_code == 200:
            self.is_logged_in = True
            return resp.json()
        else:
            assert False, "Log in failed"


def has_next_page(response):
    result = pq(response)
    next_page_links = result("a[name='nextPage']")
    return next_page_links


def parse_pages(page_list):
    result = []
    for page in page_list:
        result.extend(parse_table(page))
    return result


def parse_table(page):
    table = pq(page)
    rows = table("tr.even, tr.odd")

    result = []
    for row in rows:
        row = pq(row).children("td")
        columns = row
        date = parse_table_date(row[9])
        username = row[1].text.strip()
        modality = row[6].text.strip()
        descriptor = row[7].text.strip()
        row = {
            "date": date,
            "user": username,
            "modality": modality,
            "descriptor": descriptor,
        }
        result.append(row)
    return result


def parse_table_date(datetime_table) -> datetime:
    date_string = pq(datetime_table)("a").attr("date").split(".")[0]
    date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
    return date
