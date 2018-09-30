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
    content_pieces = soup.findAll('div', {'class': 'StoryBodyCompanionColumn'})

    content = []

    for piece in content_pieces:
        content.append(piece.text)

    return ' '.join(content)


def get_article_dicts(df_articles):
    mask = df_articles['news_source'] == 'the-new-york-times'
    df_nytimes_articles = df_articles.loc[mask]
    article_content_dicts = []

    for url in df_nytimes_articles['url']:
        article_content_dict = {}
        article_content_dict['url'] = url
        article_content_dict['content'] = get_article_content(url)

        article_content_dicts.append(article_content_dict)

    return article_content_dicts


def main():
    df_articles = pd.read_json('df_articles.json')
    articles_contents_dict = get_article_dicts(df_articles)
    print(articles_contents_dict)

main()

