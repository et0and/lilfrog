import csv
from datetime import datetime
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from tqdm import tqdm

axe = Axe()

# Get the current date and format it as dd-mm-yy
now = datetime.now()
date_string = now.strftime("%d-%m-%y")

# Open the CSV file for writing with the new name
with open(f'axe-report-{date_string}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Violations"])

    # Read the URLs from the file
    with open('urls.txt', 'r') as url_file:
        urls = [url.strip() for url in url_file]  # Remove any trailing newline and store URLs

        # Use tqdm to wrap around urls for progress bar
        for url in tqdm(urls):
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                result = axe.run(page)
                browser.close()

            violations = result.get('violations', [])
            detailed_violations = []
            for v in violations:
                detailed_violations.append(f"{v['id']} - {v['description']} (Line {v['nodes'][0]['line']})")
            writer.writerow([url, ', '.join(detailed_violations)])
            tqdm.write(f"{len(violations)} violations found on {url}")  # Use tqdm.write for print