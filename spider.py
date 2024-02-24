import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
from tqdm import tqdm

def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

def get_links(url):
    try:
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        return [url.get('href') for url in soup.find_all('a', href=True)]
    except requests.exceptions.RequestException:
        return []

# Get the current date
now = datetime.now()
date_string = now.strftime("%d-%m-%Y")

# Initialize CSV file with headers
filename = f'link-report-{date_string}.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parent URL", "URL", "Status"])

# Ask for the URL to scan
url_to_scan = input("Please enter the URL to scan: ")

# List to store visited URLs
visited_urls = []

# Recursively scan the website
def scan_website(parent_url, url):
    if url in visited_urls:
        return
    visited_urls.append(url)
    status = "working" if check_url(url) else "broken"
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([parent_url, url, status])
    for link in tqdm(get_links(url)):
        if link.startswith(url_to_scan):
            scan_website(url, link)

scan_website(url_to_scan, url_to_scan)
