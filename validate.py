from bs4 import BeautifulSoup
import requests
import sys
import re

def get_xml_content(path):
    file = open(path, 'rb')
    content = file.read().decode('utf8')
    file.close()
    return content


def extract_links_from_sitemap(xml):
    links = []
    soup = BeautifulSoup(xml, "html.parser")
    url_tags = soup.find_all("url")
    for url_tag in url_tags:
        links.append(url_tag.findNext("loc").text)
    return links


def validate(link):
    try:
        response = requests.get(link)
        return response.status_code
    except requests.exceptions.RequestException as e:
        return 404


if __name__ == "__main__":
    arguments = sys.argv
    xml = get_xml_content(arguments[1])
    current_domain = arguments[2]
    test_domain = arguments[3]
    xml = re.sub(current_domain, test_domain, xml, re.M)
    for l in extract_links_from_sitemap(xml):
        print(f'{validate(l)} - {l}')
