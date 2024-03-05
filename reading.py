import requests
from bs4 import BeautifulSoup
import csv
import re
import textstat
from progiter import ProgIter

# Function to convert the Flesch Reading Ease score to a text description
def get_readability_label(score):
    if score >= 90:
        return "Very Easy"
    elif score >= 80:
        return "Easy"
    elif score >= 70:
        return "Fairly Easy"
    elif score >= 60:
        return "Standard"
    elif score >= 50:
        return "Fairly Difficult"
    elif score >= 30:
        return "Difficult"
    else:
        return "Very Confusing"

# Function to write a batch of results to the CSV file
def write_results_to_csv(writer, results_batch):
    for result in results_batch:
        writer.writerow(result)

# Read single/multiple URLs from a text file
with open("urls.txt", "r") as f:
    urls = [line.strip() for line in f]

# Initialize CSV file for output
with open("output.csv", "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["URL", "Flesch Kincaid Score", "Readability Label"])  # Updated to include Readability Label

    results_batch = []  # Initialize a list to store results for batch processing
    batch_size = 10     # Define batch size; adjust this number based on your needs

    # Iterate through URLs using ProgIter
    for url in ProgIter(urls, verbose=2):  # Use ProgIter here
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

            # Calculate Flesch Kincaid readability score and get the text label
            fk_score = textstat.flesch_reading_ease(text_content)
            readability_label = get_readability_label(fk_score)
            results_batch.append([url, fk_score, readability_label])  # Include readability label in the results

        except requests.exceptions.RequestException as e:
            print(f"Error making request to URL: {url}, {e}")
            results_batch.append([url, "Error making request", "N/A"])
        except textstat.TextStatError as e:
            print(f"Error calculating Flesch Kincaid score for URL: {url}, {e}")
            results_batch.append([url, "Error calculating score", "N/A"])
        except Exception as e:
            print(f"Unexpected error processing URL: {url}, {e}")
            results_batch.append([url, "Unexpected error", "N/A"])

        # Write results in batches
        if len(results_batch) >= batch_size:
            write_results_to_csv(writer, results_batch)
            results_batch = []  # Reset the results batch after writing

    # Write any remaining results that did not fill up the last batch
    if results_batch:
        write_results_to_csv(writer, results_batch)