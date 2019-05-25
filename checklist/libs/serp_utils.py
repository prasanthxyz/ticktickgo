""" Serp Utils """

import json
import requests

URL_TEMPLATE = "https://www.bingapis.com/api/v7/search?q=%s&appid=%s&count=%s"

DOMAIN_BLACKLIST = ["travel.stackexchange.com", "quora.com", "oyorooms.com"]


def filter_blacklist(url):
    """ filter blacklisted urls out """
    return url and all(domain not in url for domain in DOMAIN_BLACKLIST)


def get_serp_links(query_string, app_id, num_urls=10):
    """ Extract first num_urls (default 10) urls from SERP response """
    if not query_string:
        return []

    url = URL_TEMPLATE % (requests.utils.requote_uri(query_string), app_id, num_urls)
    try:
        serp_data_json = requests.get(url).text
    except Exception:
        return []
    serp_data = json.loads(serp_data_json)
    web_pages = serp_data.get('webPages').get('value')
    if not web_pages:
        return []

    urls = [str(web_page.get('url')) for web_page in web_pages]
    return filter(filter_blacklist, urls)

if __name__ == "__main__":
    links = get_serp_links('checklist for travelling to ooty', 20)
    for link in links:
        print(link)
