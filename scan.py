import asyncio
import csv
from urllib.parse import urljoin, urlparse
from playwright.async_api import async_playwright
from tqdm.asyncio import tqdm

async def get_links(page, url):
    await page.goto(url)
    links = await page.query_selector_all('a')
    internal_links = []

    for link in links:
        href = await link.get_attribute('href')
        parsed_href = urlparse(href)
        if parsed_href.netloc == "" or parsed_href.netloc == urlparse(url).netloc:
            internal_links.append(urljoin(url, href))

    return internal_links

async def check_link(page, link):
    try:
        response = await page.goto(link, timeout=10000, wait_until='networkidle')
        return link, response.status
    except Exception as e:
        return link, "Error"

async def write_to_csv(rows, output_file):
    with open(output_file, 'w', newline='') as csvfile:
        fieldnames = ['Parent URL', 'URL Affected', 'Status Code']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for row in rows:
            writer.writerow(row)

async def crawl_website(page, url, results, internal_links):
    links = await get_links(page, url)

    for link in links:
        internal_links.add(link)

    async with tqdm(total=len(internal_links)) as pbar:
        for link in internal_links:
            if link not in results:
                result = await check_link(page, link)
                results.append({'Parent URL': url, 'URL Affected': result[0], 'Status Code': result[1]})
                await crawl_website(page, result[0], results, internal_links)
                pbar.update(1)

async def main():
    input_url = input("Enter the URL to check for broken links: ")
    output_file = "broken_links.csv"

    async with async_playwright() as playwright:
        browser = await playwright.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()

        results = []
        internal_links = set()

        await crawl_website(page, input_url, results, internal_links)

        await context.close()
        await browser.close()

        await write_to_csv(results, output_file)
        print(f"Results saved to {output_file}")

asyncio.run(main())