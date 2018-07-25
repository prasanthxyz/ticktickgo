"""
Extract keywords for checklist generator from a website
"""

import requests
import html2text


def filter_required_lines(line):
    """ Filter out lines to consider """
    line = line.strip()
    return line and (line.startswith('*') or line.startswith('#'))


def process_lines(line):
    """ Strip the line off unrequired characters """
    return line.lstrip('0123456789\\.*#/ \n')


def html2keywords(url):
    """ get keywords in a webpage """
    html_to_text = html2text.HTML2Text()
    html_to_text.ignore_images = True
    html_to_text.ignore_emphasis = True
    html_to_text.ignore_links = True
    html_to_text.ignore_tables = True

    try:
        html_data = requests.get(url).text.encode('ascii', errors='ignore')
    except Exception:
        return []

    markdown_data = html_to_text.handle(html_data).encode('utf-8')
    markdown_lines = [line for line in markdown_data.split('\n') if line]
    required_lines = filter(filter_required_lines, markdown_lines)
    processed_lines = [line for line in map(process_lines, required_lines) if line]
    print "Processed url:", url
    return processed_lines


if __name__ == "__main__":
    print html2keywords('http://www.estrelahotels.com/blog/things-to-pack-for-goa-trip/')
    print html2keywords('https://www.indianholiday.com/blog/useful-tips-goa-trip/')
