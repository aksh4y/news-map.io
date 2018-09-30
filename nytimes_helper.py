import requests
import re
from bs4 import BeautifulSoup
import pandas as pd


def retrieve_article_data(begin_date, end_date, pages, key):
    url = 'https://api.nytimes.com/svc/search/v2/articlesearch.json?'

    df_articles = pd.DataFrame(data={'url': [],
                                 'url_image': [],
                                 'article': [],
                                 'datetime': [],
                                 'news_source': [],
                                 'content': []
                                 })

    params = {'api-key': key,
             'begin_date': begin_date,
             'end_date': end_date}

    for key, value in params.items():
        url += key + '=' + value + '&'

    for page in range(pages):
        page_url = url + 'page' + '=' + str(page)

        json_response = requests.get(page_url).json()

        if json_response['status'] == 'OK':
            for article in json_response['response']['docs']:
                web_url = article['web_url']
                full_content = get_article_content(web_url)
                url_image = get_article_image(web_url)

                df_articles = df_articles.append({'url': web_url,
                                                 'url_image': url_image,
                                                 'article': article['headline']['main'],
                                                 'datetime': article['pub_date'],
                                                 'news_source': article['source'],
                                                 'content': full_content}, ignore_index=True)

    return df_articles


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
        cleaned_content = re.sub('[^0-9a-zA-Z]+', ' ', piece.text).strip()
        content.append(cleaned_content)

    return ' '.join(content)


def get_article_image(url):
    url = url.replace('\\/', '/')
    page = requests.get(url)

    try:
        page.raise_for_status()
    except Exception as exc:
        print('Problem downloading: %s' % exc)

    soup = BeautifulSoup(page.text, 'html.parser')
    url_image = soup.find('img').get('src')

    return url_image


def get_article_dicts(df_articles):
    article_content_dicts = []

    for url in df_articles['url']:
        article_content_dict = {}
        article_content_dict['url'] = url
        article_content_dict['content'] = get_article_content(url)

        article_content_dicts.append(article_content_dict)

    return article_content_dicts


def main():
    df_articles = retrieve_article_data('20180922', '20180929', 15, '64421d7edeab4ab9ad0ceea49bfcef03')
    articles_contents_dict = get_article_dicts(df_articles)
    print(articles_contents_dict)
    print(len(articles_contents_dict))


main()
