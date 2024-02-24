import requests
from axe_core_python import AxeResults
from axe_core_python.commons.checks import CheckSettings
from axe_core_python.commons.htmlcs import HTMLCodeSnippet
from axe_core_python.selenium_python import driver_factory
from selenium.webdriver.chrome.options import Options
import csv
import datetime
from tqdm import tqdm

def scan_url(url):
chrome_options = Options()
chrome_options.add_argument('--headless')
driver = driver_factory.create_driver(chrome_options=chrome_options)
driver.get(url)

results = AxeResults()
check_settings = CheckSettings()
html_cs = HTMLCodeSnippet(driver.page_source)
results = html_cs.run_rules(check_settings)

issues = ', '.join([issue["description"] for issue in results.violations])
driver.quit()
return issues

with open('urls.txt', 'r') as file:
urls = file.readlines()

output_filename = f'axe-report-{datetime.datetime.now().strftime("%d-%m-%Y")}.csv'
with open(output_filename, 'w', newline='') as csvfile:
fieldnames = ['url', 'issues']
writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
writer.writeheader()

for url in tqdm(urls):
    issues = scan_url(url.strip())
    writer.writerow({'url': url.strip(), 'issues': issues})
