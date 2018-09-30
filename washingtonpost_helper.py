import requests
from bs4 import BeautifulSoup
import pandas as pd


def get_article_content(url):
    url = url.replace('\\/', '/')
    page = requests.get(url)

    try:
        page.raise_for_status()
    except Exception as exc:
        print('Problem downloading: %s' % exc)

    soup = BeautifulSoup(page.text, 'html.parser')
    content_pieces = soup.findAll('p')

    content = []

    for piece in content_pieces:
        content.append(piece.text)

    return ' '.join(content)

if __name__ == "__main__":
    print(get_article_content('https://www.washingtonpost.com/news/local/wp/2018/09/28/feature/they-was-killing-black-people/?utm_term=.a6157a1acdcd'))
