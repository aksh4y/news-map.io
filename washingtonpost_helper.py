import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from location_helper import insert_location_into_articles
from collections import defaultdict
import datetime
import numpy as np

def retrieve_article_data():
    df_articles = pd.read_json('df_articles.json')

    mask = df_articles['news_source'] == 'the-washington-post'
    df_washingtonpost_articles = df_articles.loc[mask]

    for index, row in df_washingtonpost_articles.head(20).iterrows():
        df_washingtonpost_articles.at[index, 'content'] = get_article_content(row['url'])

    return df_washingtonpost_articles.head(20)

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
        cleaned_content = re.sub('[^0-9a-zA-Z]+', ' ', piece.text).strip()
        content.append(cleaned_content)

    return ' '.join(content)

def get_article_dicts(df_articles):
    article_content_dicts = []

    for index, row in df_articles.iterrows():
        article_content_dict = {}
        article_content_dict['url'] = row['url']
        article_content_dict['content'] = row['content']
        article_content_dict['article'] = row['article']
        article_content_dicts.append(article_content_dict)

    return article_content_dicts

def get_articles_coordinates(cache):
    from pprint import pprint
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')

    df_articles = retrieve_article_data()
    articles_contents_list = get_article_dicts(df_articles)
    locations_included_list = insert_location_into_articles(articles_contents_list, cache)
    ret = defaultdict(list)
    for article in locations_included_list:
        for location in article['location']:
            if location == None:
                continue
            pic_link = 'https://eig.org/wp-content/uploads/2016/06/washington-post-logo.jpg'
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

if __name__ == "__main__":
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=7)
    start_date = start_date.strftime('%Y%m%d')
    end_date = end_date.strftime('%Y%m%d')
    df_articles = retrieve_article_data()
    print(np.array(df_articles.head(5)))
