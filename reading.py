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
            response.raise_for_status()  # Raise an exception for non-200 status codes

            soup = BeautifulSoup(response.text, "html.parser")

            # Extract and clean the text content. Assumes that content is in a standard p or article tag.
            text_content = " ".join(
                [p.get_text(separator=" ", strip=True) for p in soup.find_all(["p", "article", "h1", "h2", "h3", "h4", "li"])]
            )
            text_content = re.sub(r"\s+", " ", text_content).strip()

            # Calculate Flesch Kincaid readability score
            fk_score = textstat.flesch_reading_ease(text_content)
            writer.writerow([url, fk_score])  # Don't forget to write the score to the CSV
        except requests.exceptions.RequestException as e:
            print(f"Error making request to URL: {url}, {e}")
        except textstat.TextStatError as e:
            print(f"Error calculating Flesch Kincaid score for URL: {url}, {e}")
        except Exception as e:
            print(f"Unexpected error processing URL: {url}, {e}")
