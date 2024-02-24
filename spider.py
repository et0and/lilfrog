import requests
import csv
from datetime import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup

def check_url(url, parent_url=None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # If the URL is working, find and return any links in the URL
            soup = BeautifulSoup(response.text, 'html.parser')
            return [(parent_url, link.get('href')) for link in soup.find_all('a', href=True)]
        return []
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

# Read the initial URLs
with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

# Use a queue to hold URLs to check
to_check = urls[:]

while to_check:
    url = to_check.pop(0)
    links = check_url(url)
    for parent_url, link in links:
        # Write the result to the CSV file
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([parent_url, link, "working"])
        to_check.append(link)
