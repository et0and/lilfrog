import requests
import csv
from datetime import datetime
from tqdm import tqdm
from bs4 import BeautifulSoup
from collections import deque

def check_url(url, parent_url=None):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            return [(parent_url, link.get('href')) for link in soup.find_all('a', href=True)]
        return []
    except requests.exceptions.RequestException:
        return []

now = datetime.now()
date_string = now.strftime("%d-%m-%Y")

filename = f'link-report-{date_string}.csv'
with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Parent URL", "URL", "Status"])

with open('urls.txt', 'r') as file:
    urls = [line.strip() for line in file.readlines()]

queue = deque(urls)
checked_count = 0
total_urls = len(urls)

while queue:
    url = queue.popleft()
    links = check_url(url)
    for parent_url, link in links:
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([parent_url, link, "working"])
        queue.append(link)
        total_urls += 1
    checked_count += 1
    tqdm.write(f"Checked {checked_count}/{total_urls}")
    tqdm.update()