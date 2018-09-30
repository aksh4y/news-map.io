import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

def get_article_content(url):
    url = url.replace('\\/', '/')
    page = requests.get(url)

    try:
        page.raise_for_status()
    except Exception as exc:
        print('Problem downloading: %s' % exc)

    soup = BeautifulSoup(page.text, 'html.parser')
    content_types = ['div', 'p', 'h1', 'h2', 'h3', 'h4']
    content_classes = ['zn-body__paragraph', 'Paragraph__component', 'speakable']
    content_pieces = soup.findAll(content_types, {'class': content_classes}) + soup.findAll(content_types[1:])

    content = []

    for piece in content_pieces:
        cleaned_content = re.sub('[^0-9a-zA-Z]+', ' ', piece.text).strip()
        content.append(cleaned_content)

    return ' '.join(content)

if __name__ == "__main__":
    print(get_article_content('https://money.cnn.com/2018/09/29/technology/business/elon-musk-tesla-sec-settlement/index.html'))
