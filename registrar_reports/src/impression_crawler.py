from datetime import datetime

import pandas as pd
import requests
from pandas import DataFrame
from pyquery import PyQuery as pq


class InteleBrowserCrawler:
    FRAME_TIMEOUT = 2 * 60 * 1000

    def __init__(self, config, users) -> None:
        # base64 decode
        self.username: str = config["LOGIN"]
        self.password: str = config["IVPW"]
        self.cdhb_pass: str = config["CDHBPW"]
        self.base_url: str = config["IB_URL"]
        self.is_logged_in: bool = False
        self.detailed: bool = True
        self.users = users.dropna()

    def run(self) -> DataFrame:
        with requests.Session() as s:
            s.auth = (self.username, self.cdhb_pass)
            s.trust_env = False
            self.session = s
            self._log_in()
            return self._iter_users()

    def _iter_users(self) -> DataFrame:
        result = []
        for _, user in self.users.iterrows():
            if user.Start:
                data = self._query_user(user.Username, user.Start, user.End)
                result.extend(data)
        assert result, "Empty result, something went wrong"
        result = [x for x in result if x is not None]
        df = DataFrame(result)
        return df

    def _query_user(self, username, start, end) -> list:
        start_input: str = start.strftime("%Y/%m/%d")
        end_input: str = end.strftime("%Y/%m/%d")

        if cache := self.retrieve_cache(username, start, end):
            return cache

        print(f"Current user: {username}", end="\n")
        print(f"Date range: {start_input} - {end_input}", end="\n\n")

        first_page = self._get_first_page(username, start_input, end_input)
        subsequent_pages = self._get_subsequent_pages(first_page)
        all_pages = [first_page] + subsequent_pages

        print("A total of ", len(all_pages), " retrieved", end="\n")

        result = self._parse_tables(all_pages)
        self.save_cache(result)
        return result

    def _get_first_page(self, username, start, end) -> str:
        response = self.session.post(
            f"{self.base_url}/app",
            data={
                "service": "direct/1/AuditDetails/$Form",
                "sp": "S0",
                "Form0": "usernameFilter,$PropertySelection,patientIdFilter,studyDescriptionFilter,$PropertySelection$0,$Checkbox,$Checkbox$0,$Checkbox$1,$Checkbox$2,$Checkbox$3,$Checkbox$4,$Checkbox$5,$Checkbox$6,$Checkbox$7,$Checkbox$8,$Checkbox$9,$Checkbox$10,$Checkbox$11,$Checkbox$12,$Checkbox$13,$Checkbox$14,$Checkbox$15,$Checkbox$16,$Checkbox$17,$Checkbox$18,$Checkbox$19,$Checkbox$20,$Checkbox$21,$Checkbox$22,$Checkbox$23,$Checkbox$24,$Checkbox$25,$Checkbox$26,$Checkbox$27,$Checkbox$28,$Checkbox$29,$Checkbox$30,$Checkbox$31,$Checkbox$32,$Checkbox$33,$Checkbox$34,$Checkbox$35,$Checkbox$36,$Checkbox$37,$Checkbox$38,$Checkbox$39,$Checkbox$40,$Checkbox$41,$Checkbox$42,$Submit",
                "usernameFilter": username,
                "$PropertySelection": "anyRole",
                "patientIdFilter": "",
                "studyDescriptionFilter": "",
                "$PropertySelection$0": f"{start}:{end}",
                "$Checkbox$2": "on",
                "$Checkbox$9": "on",
                "$Submit": "Update",
            },
        )
        return response.content.decode("utf-8")

    def _get_subsequent_pages(self, first_page) -> list[str]:
        current_page = first_page
        result = []

        while self._has_next_page(current_page):
            print("Retrieving the next page..")
            response = self.session.get(
                f"{self.base_url}/app?service=direct/1/AuditDetails/auditDetailsTable.customPaginationControlTop.nextPage"
            )
            current_page = response.content.decode("utf-8")
            print("Another page retrieved successfully")
            result.append(current_page)

        return result

    def save_cache(self, result):
        # todo: implement cache
        pass

    def retrieve_cache(self, username, start, end):
        # todo: implement cache
        return False

    def _log_in(self):
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
            raise Exception("Log in failed")

    def _has_next_page(self, response):
        result = pq(response)
        next_page_links = result("a[name='nextPage']")
        return next_page_links

    def _parse_tables(self, page_list):
        result = []
        for page in page_list:
            result.extend(self._parse_table(page))
        return result

    def _parse_table(self, page):
        table = pq(page)
        rows = table("tr.even, tr.odd")

        result = []
        for row in rows:
            row = pq(row).children("td")
            parsed_row = self.parse_row(row)
            result.append(parsed_row)
        return result

    def parse_row(self, row):
        date = self._parse_row_date(row[9])
        username = row[1].text.strip()
        action = row[3].text.strip()
        modality = row[6].text.strip()
        descriptor = row[7].text.strip()

        if not descriptor:
            # skip empty rows
            return None

        if self.detailed:
            extra_info = self._get_extra_details(row)
            study_date = pq(extra_info)("sp")[0].text.strip()
            accession_no = pq(extra_info)("sp")[1].text.strip()
            referring_doctor = pq(extra_info)("sp")[3].text.strip()
            row = self.build_record(
                date,
                username,
                action,
                modality,
                descriptor,
                accession_no,
                study_date,
                referring_doctor,
            )
        else:
            row = self.build_record(date, username, action, modality, descriptor)
        return row

    def _parse_row_date(self, datetime_table) -> datetime:
        date_string = pq(datetime_table)("a").attr("date").split(".")[0]
        date = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return date

    def _get_extra_details(self, row):
        """Mostly used to get the study date and accession number"""
        more_info_button = row[9]
        uid = pq(more_info_button)("a").attr("studyuid")
        response = self.session.get(
            f"{self.base_url}/app",
            params={"service": "xtile/null/AuditDetails/$XTile$2", "sp": uid},
        )
        return response.content

    def build_record(
        self,
        date,
        username,
        action,
        modality,
        description,
        accession_no="",
        study_date=None,
        referring_doctor="",
    ):
        return {
            "date": date,
            "user": username,
            "action": action,
            "modality": modality,
            "descriptor": description,
            "accession_no": accession_no,
            "study_date": study_date,
            "referring_doctor": referring_doctor,
        }
