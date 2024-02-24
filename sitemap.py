import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin, urlparse

def crawl(url, domain):
    visited_links = set()
    links_to_visit = [url]

    while links_to_visit:
        current_url = links_to_visit.pop(0)
        if current_url not in visited_links:
            try:
                response = requests.get(current_url)
                response.raise_for_status()  # Raise an HTTPError if the HTTP request returned an unsuccessful status code
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a', href=True):
                    href = link.get('href')
                    # Make sure href is not None and is not a fragment or mailto link
                    if href and not href.startswith('#') and not href.startswith('mailto:') and not href.startswith('tel:'):
                        full_link = urljoin(current_url, href)
                        # Check if the link is within the same domain
                        if urlparse(full_link).netloc == urlparse(domain).netloc:
                            if full_link not in visited_links:
                                links_to_visit.append(full_link)

                visited_links.add(current_url)
            except requests.exceptions.RequestException as e:
                print(f"Error with URL {current_url}: {e}")

    return visited_links

def generate_sitemap_xml(links, output_file='sitemap.xml'):
    urlset = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for link in links:
        url = etree.SubElement(urlset, 'url')
        loc = etree.SubElement(url, 'loc')
        loc.text = link

    xml_data = etree.tostring(urlset, encoding='utf-8', xml_declaration=True, pretty_print=True)

    with open(output_file, 'wb') as f:
        f.write(xml_data)

if __name__ == '__main__':
    user_url = input("Enter the URL to crawl (including 'http(s)://'): ")
    parsed_domain = urlparse(user_url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_domain)
    crawled_links = crawl(user_url, domain)
    generate_sitemap_xml(crawled_links)
    print(f"Sitemap generated as sitemap.xml")