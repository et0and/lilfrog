import csv
import argparse
from concurrent.futures import ThreadPoolExecutor
from playwright.sync_api import sync_playwright
from axe_core_python.sync_playwright import Axe
from tqdm import tqdm

def analyze_url(url):
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page()
        
        try:
            # Set a generous timeout for navigation if the sites are slow to load
            page.goto(url, timeout=60000)
            result = axe.run(page)
            violations = result.get('violations', [])
            tqdm.write(f"{len(violations)} violations found on {url}")
            return url, ', '.join([str(v) for v in violations])
        except Exception as e:
            # Handle exceptions, like timeouts, and log them
            tqdm.write(f"Timeout or other error occurred while visiting {url}: {e}")
            return url, "Error occurred"
        finally:
            # Ensure the page is closed after each iteration
            page.close()
            browser.close()

def main(threads):
    axe = Axe()
    # Open the CSV file for writing
    with open('results.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["URL", "Violations"])

        # Read the URLs from the file
        with open('urls.txt', 'r') as url_file:
            urls = [url.strip() for url in url_file]  # Remove any trailing newline and store URLs

        # Use ThreadPoolExecutor to run axe analysis in parallel
        with ThreadPoolExecutor(max_workers=threads) as executor:
            # Use tqdm to wrap around executor for progress bar
            for result in tqdm(executor.map(analyze_url, urls), total=len(urls)):
                writer.writerow(result)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run axe analysis on a list of URLs.")
    parser.add_argument('-t', '--threads', type=int, default=1, help="Number of threads to use")
    args = parser.parse_args()

    main(args.threads)