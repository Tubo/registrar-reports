import time
import os
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright
import pandas as pd

load_dotenv()

USERNAME = os.getenv("LOGIN")
PASSWORD = os.getenv("IVPW")
CDHBPW = os.getenv("CDHBPW")

SIGNIN_URL = "http://159.117.33.41/InteleBrowser/app"
AUDIT_URL = "http://159.117.33.41/InteleBrowser/app?service=direct/1/AuditDetails/auditDetailsTable.customPaginationControlTop.nextPage"

FRAME_TIMEOUT = 2 * 60 * 1000


def run(playwright: Playwright, usernames, start, end) -> None:
    browser = playwright.chromium.launch(headless=False, slow_mo=50)
    context = browser.new_context(
        http_credentials={"username": USERNAME, "password": CDHBPW}
    )

    # Open InteleBrowser and log in
    page = context.new_page()
    page.goto(SIGNIN_URL)
    log_in(page, USERNAME, PASSWORD)
    page.goto(AUDIT_URL)

    # Start auditing
    fn = (
        f"impression_crawler/output/{start.replace('/', '')}-{end.replace('/', '')}.pkl"
    )
    try:
        prev_results = pd.read_pickle(fn)
    except FileNotFoundError:
        prev_results = pd.DataFrame()

    results = [] if prev_results is None else [prev_results]

    for username in usernames:
        if not prev_results.empty and username in " ".join(prev_results.user.unique()):
            continue
        rows = audit(page, username, start, end)
        df = pd.DataFrame(rows)
        results.append(df)
    combined_results = pd.concat(results)
    combined_results.to_pickle(fn)  # save result

    # Shutdown
    context.close()
    browser.close()

    return combined_results


def load_usernames(path):
    users = pd.read_csv(path, comment="#")
    return users


def log_in(page, username, password):
    # Fill [placeholder="Username"]
    page.fill('[placeholder="Username"]', username)
    # Fill [placeholder="Password"]
    page.fill('[placeholder="Password"]', password)
    # Click button
    # with page.expect_navigation(url="http://159.117.33.41/InteleBrowser/app?_page_ts_=1645969601922"):
    with page.expect_navigation():
        page.click("button")


def audit(page, username, start, end) -> list:
    # Fill in query form
    fill_form(page, username, start, end)

    # Wait for load completion
    wait = 10
    while not user_table_loaded(page, username) and wait:
        print(f"Results for {username} not loaded, wait for 1 second")
        time.sleep(1)
        wait -= 1
    print("First page loaded")

    # Parse the first page
    results = []
    results.extend(parse_table(page))

    # Parse the subsequent pages
    nextPage_button = page.locator(".tablecontrol a[name=nextPage]")
    while nextPage_button.count() > 0:
        page.goto(AUDIT_URL)
        page_result = parse_table(page)
        results.extend(page_result)
    return results


def fill_form(page, username, start, end):
    # Fill input[name="usernameFilter"]
    page.fill('input[name="usernameFilter"]', username)
    # Click text=Add Emergency Impression
    page.check("text=Add Emergency Impression")
    # Select custom date
    page.select_option('select[name="\\$PropertySelection\\$0"]', "defineCustomDates")
    # Fill text=From To >> input[type="text"]
    page.fill('text=From To >> input[type="text"]', start)
    # Fill #toDateField
    page.fill("#toDateField", end)
    # Click text=OK
    page.click("text=OK")
    # Select 1000 per page: option '4' for 1000
    # page.select_option('select[name="pageSizeSelect"]', "2")
    # Click text=Update
    page.click("input.button.updateButton", timeout=60000)


def user_table_loaded(page, username) -> bool:
    parsed_table = parse_table(page)
    if parsed_table:
        row_match_user = [username in row.get("user") for row in parsed_table]
        print("Check loading for ", username, ":", all(row_match_user))
        return all(row_match_user)
    return False


def parse_table(page) -> list:
    rows = page.locator(
        "table#searchResultsMainTable > tbody > tr.even, table#searchResultsMainTable > tbody > tr.odd",
        has_text="Impression",
    )
    content = rows.all_inner_texts()
    count = len(content)
    print(f"Page has {count} entries... starting parsing now")
    results = []
    for row in content:
        items = row.split("\t")
        items = [item.strip() for item in items]
        if parsed_row := parse_row(items):
            results.append(parsed_row)
    return results


def parse_row(row) -> dict:
    if row:
        return {
            "date": row[0],
            "time": row[1],
            "user": row[2],
            "modality": row[7],
            "descriptor": row[8],
        }


if __name__ == "__main__":
    start = "2021/11/30"
    end = "2022/05/21"
    print(USERNAME, PASSWORD)
    usernames = load_usernames("impression_crawler/username_mapping.csv").username

    with sync_playwright() as playwright:
        df = run(playwright, usernames, start, end)
        summary = df.groupby("user").modality.value_counts()
        pd.DataFrame(summary).to_string(
            f"impression_crawler/output/{start.replace('/', '')}-{end.replace('/', '')}.txt"
        )
