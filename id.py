import re

# Define a regular expression pattern for URLs with specific domain extensions
# This pattern looks for strings containing .govt, .nz, .com, .org, or .net
url_pattern = r'\b\w+\.(?:govt|nz|com|org|net)\b(?:[^\s]*\b)?'

# Read the content of the HTML file
with open('yourfile.html', 'r', encoding='utf-8') as file:
    content = file.read()

# Find all matches of the URL pattern
urls = re.findall(url_pattern, content)

# Print or process the URLs
for url in urls:
    print(url)

# Optionally, save the URLs to a file
with open('extracted_urls.txt', 'w', encoding='utf-8') as output_file:
    for url in urls:
        output_file.write(url + '\n')