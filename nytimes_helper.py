import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
from location_helper import insert_location_into_articles
from collections import defaultdict
import datetime

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

    for index, row in df_articles.iterrows():
        article_content_dict = {}
        article_content_dict['url'] = row['url']
        article_content_dict['content'] = row['content']
        article_content_dict['article'] = row['article']
        article_content_dicts.append(article_content_dict)

    return article_content_dicts

def get_nytimes_articles_coordinates(cache):
    from pprint import pprint
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')
    # Get n pages from the past week from NYTimes API
    df_articles = retrieve_article_data(start_date, end_date, 1, '64421d7edeab4ab9ad0ceea49bfcef03')
    articles_contents_list = get_article_dicts(df_articles)
    locations_included_list = insert_location_into_articles(articles_contents_list, cache)
    ret = defaultdict(list)
    for article in locations_included_list:
        for location in article['location']:
            if location == None:
                continue
            pic_link = '/'.join(article.get('url', '///').split('/')[:3]) + '/favicon.ico'
            ret[str(location.get('coordinates').get('lng'))+','+str(location.get('coordinates').get('lat'))].append({
                    'url': article.get('url', ''),
                    'title': article.get('article', ''),
                    'pic': pic_link
                })
    return ret

def get_dict_to_csv(json_results):
    articles_coords_dict = json_results
    csv = 'lng,lat,url,title,pic\n'
    for coord in articles_coords_dict:
        for article in articles_coords_dict[coord]:
            csv += coord
            csv += ','.join([article.get('url', ''), article.get('article', ''), article.get('url_image', '')]) + '\n'
    return csv

if __name__ == '__main__':
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')
    df_articles = retrieve_article_data(start_date, end_date, 1, '64421d7edeab4ab9ad0ceea49bfcef03')
    import numpy as np
    print(np.array(df_articles.head(5)))
