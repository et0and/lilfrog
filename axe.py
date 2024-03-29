import csv
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from tqdm import tqdm

axe = Axe()

# Open the CSV file for writing
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Violations"])

    # Read the URLs from the file
    with open('urls.txt', 'r') as url_file:
        urls = [url.strip() for url in url_file]  # Remove any trailing newline and store URLs

    # Use tqdm to wrap around urls for progress bar
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()

        for url in tqdm(urls):
            try:
                page = browser.new_page()
                # Set a generous timeout for navigation if the sites are slow to load
                page.goto(url, timeout=60000)
                result = axe.run(page)
                violations = result.get('violations', [])
                writer.writerow([url, ', '.join([str(v) for v in violations])])
                tqdm.write(f"{len(violations)} violations found on {url}")
            except Exception as e:
                # Handle exceptions, like timeouts, and log them
                tqdm.write(f"Timeout or other error occurred while visiting {url}: {e}")
            finally:
                # Ensure the page is closed after each iteration
                page.close()
                
        browser.close()