#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
import csv
import re
import textstat
from tqdm import tqdm

# Read single/multiple URLs from a text file
with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f]

# Initialize CSV file for output
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Flesch Kincaid Score"])

    # Iterate through URLs
    for url in tqdm(urls):  # Add tqdm here
        try:
            # Fetch the webpage content
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            # Extract and clean the text content. Assumes that content is in a standard p or article tag.
            text_content = " ".join(
                [p.text for p in soup.find_all(["p", "article", "h1", "h2", "h3", "h4", "li"])]
            )
            text_content = re.sub(r"[^\w\s]", "", text_content)
            text_content = re.sub(r"\s+", " ", text_content).strip()

            # Calculate Flesch Kincaid readability score
            fk_score = textstat.flesch_reading_ease(text_content)
            writer.writerow([url, fk_score])  # Don't forget to write the score to the CSV
        except Exception as e:
            print(f"Error processing URL: {url}, {e}")
