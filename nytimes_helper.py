import requests
from bs4 import BeautifulSoup
import pandas as pd
from location_helper import insert_location_into_articles
from collections import defaultdict

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

def get_nytimes_articles_coordinates(cache):
    from pprint import pprint
    df_articles = pd.read_json('df_articles.json')
    articles_contents_list = get_article_dicts(df_articles)
    locations_included_list = insert_location_into_articles(articles_contents_list[:1], cache)
    ret = defaultdict(list)
    for article in locations_included_list:
        for location in article['location']:
            if location == None:
                continue
            ret[str(location.get('coordinates').get('lng'))+','+str(location.get('coordinates').get('lat'))].append({
                    'url': article.get('url', ''),
                    'title': article.get('article', ''),
                    'pic': article.get('url_image', '')
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
