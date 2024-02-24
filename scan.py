import requests
import csv
from datetime import datetime
from tqdm import tqdm

def check_url(url):
    try:
        response = requests.get(url)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Get the current date
now = datetime.now()
date_string = now.strftime("%d-%m-%Y")

# Initialize CSV file with headers
filename = f'link-report-{date_string}.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parent URL", "URL", "Status"])

with open('urls.txt', 'r') as file:
    urls = file.readlines()

# Use tqdm to add a progress bar
for line in tqdm(urls):
    parent_url, url = line.strip().split(',')
    status = "working" if check_url(url) else "broken"

    # Write the result to the CSV file
    with open(filename, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([parent_url, url, status])
