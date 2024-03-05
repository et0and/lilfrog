import asyncio
import csv
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from collections import deque

async def get_links(page, url):
    await page.goto(url)
    links = await page.query_selector_all('a')
    internal_links = set()

    for link in links:
        href = await link.get_attribute('href')
        if href:
            parsed_href = urlparse(href)
            if parsed_href.netloc == "" or parsed_href.netloc == urlparse(url).netloc:
                internal_links.add(urljoin(url, href))

    return internal_links

async def check_link(page, link, timeout=50000):
    try:
        response = await page.goto(link, timeout=timeout, wait_until='domcontentloaded')
        await page.wait_for_timeout(10000)  # Wait for 5 seconds
        return link, response.status
    except Exception as e:
        print(f"Error visiting {link}: {e}")
        return link, str(e)

async def append_to_csv(row, output_file):
    with open(output_file, 'a', newline='') as csvfile:
        fieldnames = ['Parent URL', 'URL Affected', 'Status Code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writerow(row)

async def crawl_website(page, start_url, output_file):
    visited = set()
    queue = deque([start_url])

    while queue:
        url = queue.popleft()
        if url in visited:
            continue

        visited.add(url)
        links = await get_links(page, url)
        tasks = [check_link(page, link) for link in links if link not in visited]

        results = await asyncio.gather(*tasks)
        for result in results:
            await append_to_csv({'Parent URL': url, 'URL Affected': result[0], 'Status Code': result[1]}, output_file)
            if result[1] == 200:  # Check if the status code is OK before adding to the queue
                queue.extend(links)

async def main():
    input_url = input("Enter the URL to check for broken links: ")
    output_file = "brokenlinks.csv"

    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Parent URL', 'URL Affected', 'Status Code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36")
        page = await context.new_page()

        await crawl_website(page, input_url, output_file)

        await context.close()
        await browser.close()

    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    asyncio.run(main())