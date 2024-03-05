import csv
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from progiter import ProgIter

axe = Axe()

def write_results_to_csv(writer, results_batch):
    for result in results_batch:
        writer.writerow(result)

# Open the CSV file for writing
with open('results.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["URL", "Violations"])

    # Read the URLs from the file
    with open('urls.txt', 'r') as url_file:
        urls = [url.strip() for url in url_file]  # Remove any trailing newline and store URLs

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        results_batch = []  # Initialize a list to store results for batch processing
        batch_size = 10     # Define batch size; adjust this number based on your needs

        # Use ProgIter to wrap around urls for progress bar
        for url in ProgIter(urls, verbose=2):
            try:
                page = browser.new_page()
                # Set a generous timeout for navigation if the sites are slow to load
                page.goto(url, timeout=60000)
                result = axe.run(page)
                violations = result.get('violations', [])
                results_batch.append([url, ', '.join([str(v) for v in violations])])
                print(f"{len(violations)} violations found on {url}")
            except Exception as e:
                # Handle exceptions, like timeouts, and log them
                print(f"Timeout or other error occurred while visiting {url}: {e}")
            finally:
                # Ensure the page is closed after each iteration
                page.close()

            # Write results in batches
            if len(results_batch) >= batch_size:
                write_results_to_csv(writer, results_batch)
                results_batch = []  # Reset the results batch after writing

        # Write any remaining results that did not fill up the last batch
        if results_batch:
            write_results_to_csv(writer, results_batch)

        browser.close()