import requests
from bs4 import BeautifulSoup
from lxml import etree
from urllib.parse import urljoin

def crawl(url, domain):
    visited_links = set()
    links_to_visit = [url]

    while links_to_visit:
        current_url = links_to_visit.pop(0)
        if current_url not in visited_links:
            try:
                response = requests.get(current_url)
                soup = BeautifulSoup(response.text, 'html.parser')

                for link in soup.find_all('a'):
                    href = link.get('href')
                    if href.startswith(domain) or not href.startswith('http'):
                        full_link = urljoin(domain, href)
                        if full_link not in visited_links:
                            links_to_visit.append(full_link)

                visited_links.add(current_url)
            except Exception as e:
                print(f"Error: {e}")

    return visited_links

def generate_sitemap_xml(links, output_file='sitemap.xml'):
    urlset = etree.Element('urlset', xmlns="http://www.sitemaps.org/schemas/sitemap/0.9")

    for link in links:
        url = etree.SubElement(urlset, 'url')
        loc = etree.SubElement(url, 'loc')
        loc.text = link

    xml_data = etree.tostring(urlset, encoding='unicode', xml_declaration=True, pretty_print=True)

    with open(output_file, 'w') as f:
        f.write(xml_data)

if __name__ == '__main__':
    user_url = input("Enter the URL to crawl (including 'http(s)://'): ")
    domain = user_url if user_url.endswith('/') else user_url + '/'
    crawled_links = crawl(user_url, domain)
    generate_sitemap_xml(crawled_links)
    print(f"Sitemap generated as sitemap.xml")