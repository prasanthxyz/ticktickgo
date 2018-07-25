""" Serp Utils """

import json
import urllib2

URL_TEMPLATE = "https://www.bingapis.com/api/v7/search?q=%s&appid=%s&count=%s"

def get_serp_links(query_string, app_id, num_urls=10):
    """ Extract first num_urls (default 10) urls from SERP response """
    if not query_string:
        return []

    url = URL_TEMPLATE % (urllib2.quote(query_string), app_id, num_urls)
    try:
        serp_data_json = urllib2.urlopen(url).read()
    except Exception:
        return []
    serp_data = json.loads(serp_data_json)
    web_pages = serp_data.get('webPages').get('value')
    if not web_pages:
        return []

    urls = [str(web_page.get('url')) for web_page in web_pages]
    return [url for url in urls if url]


if __name__ == "__main__":
    print get_serp_links('goa', 20)
