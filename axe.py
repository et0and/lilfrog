import csv
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe

axe = Axe()

# Open the CSV file for writing
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Violations"])

    # Read the URLs from the file
    with open('urls.txt', 'r') as url_file:
        for url in url_file:
            url = url.strip()  # Remove any trailing newline

            with sync_playwright() as playwright:
                browser = playwright.chromium.launch()
                page = browser.new_page()
                page.goto(url)
                result = axe.run(page)
                browser.close()

            violations = result.get('violations', [])
            writer.writerow([url, ', '.join([str(v) for v in violations])])
            print(f"{len(violations)} violations found on {url}")