import time
import os
from dotenv import load_dotenv
from playwright.sync_api import Playwright, sync_playwright

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

FRAME_TIMEOUT = 2 * 60 * 1000


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=True, slow_mo=50)
    context = browser.new_context()

    # Open InteleBrowser and log in
    page = context.new_page()
    page.goto("http://159.117.33.41/InteleBrowser/app")
    log_in(page, USERNAME, PASSWORD)
    page.frame(url="http://159.117.33.41/InteleBrowser/app?service=page/Menu").click(
        "text=Audit Users"
    )
    # Start auditing
    results = audit(page, "TuboS", "2021/02/23", "2022/02/27")
    print("Final counts: ", len(results))

    # Shutdown
    context.close()
    browser.close()


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
    while not user_table_loaded(page, username):
        print("Query not loaded, wait for 1 second")
        time.sleep(1)

    print("First page loaded")

    # Parse the first page
    results = []
    results.extend(parse_table(page))

    # Parse the subsequent pages
    nextPage_button = page.frame(name="Main").locator(".tablecontrol a[name=nextPage]")
    while nextPage_button.count() > 0:
        nextPage_button.first.click()
        page.frame(name="Main").wait_for_load_state(
            state="networkidle", timeout=FRAME_TIMEOUT
        )
        page_result = parse_table(page)
        results.extend(page_result)
    return results


def fill_form(page, username, start, end):
    # Fill input[name="usernameFilter"]
    page.frame(name="Main").fill('input[name="usernameFilter"]', username)
    # Click text=Add Emergency Impression
    page.frame(name="Main").click("text=Add Emergency Impression")
    # Select custom date
    page.frame(name="Main").select_option(
        'select[name="\\$PropertySelection\\$0"]', "defineCustomDates"
    )
    # Fill text=From To >> input[type="text"]
    page.frame(name="Main").fill('text=From To >> input[type="text"]', start)
    # Fill #toDateField
    page.frame(name="Main").fill("#toDateField", end)
    # Click text=OK
    page.frame(name="Main").click("text=OK")
    # Select 1000 per page: option '4' for 1000
    page.frame(name="Main").select_option('select[name="pageSizeSelect"]', "2")
    # Click text=Update
    page.frame(name="Main").click("text=Update")


def user_table_loaded(page, username) -> bool:
    row_match_user = [username in row.get("user") for row in parse_table(page)]
    print("Check loading:", row_match_user)
    return all(row_match_user)


def parse_table(page) -> list:
    rows = page.frame(name="Main").locator(
        "table#searchResultsMainTable > tbody > tr.even, table#searchResultsMainTable > tbody > tr.odd"
    )
    count = rows.count()
    print(f"Page has {count} entries... starting parsing now")
    results = []
    for i in range(count):
        row = rows.nth(i).locator(f"td.tableValues").all_text_contents()
        if parsed_row := parse_row(row):
            results.append(parsed_row)
    return results


def parse_row(row) -> dict:
    if row:
        return {
            "datetime": row[0].split(),
            "user": row[1],
            "modality": row[6],
            "descriptor": row[7].strip(),
        }


with sync_playwright() as playwright:
    run(playwright)
