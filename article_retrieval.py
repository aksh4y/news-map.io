from newsapi import NewsApiClient
import pandas as pd

df_articles = pd.DataFrame(data={'url': [],
                                 'url_image': [],
                                 'article': [],
                                 'datetime': [],
                                 'news_source': [],
                                 'content': []
                                 })

df_locations = pd.DataFrame(data={'location': [],
                                  'latitude': [],
                                  'longitude': []
                                  })

df_articles_locations = pd.DataFrame(data={'url': [],
                                           'location': []
                                           })

newsapi = NewsApiClient(api_key='c0c364cd6be242369926fbc245d6865f')
sources = newsapi.get_sources(language='en')

english_sources_ids = ['abc-news', 'al-jazeera-english', 'associated-press', 'bbc-news', 'bloomberg', 'business-insider', 'buzzfeed', 'cbs-news', 'cnn', 'engadget', 'financial-times', 'fortune', 'fox-news', 'google-news', 'hacker-news', 'independent', 'msnbc', 'national-geographic', 'nbc-news', 'new-york-magazine', 'nhl-news', 'reuters', 'techcrunch', 'techradar', 'the-economist', 'the-guardian-uk', 'the-huffington-post', 'the-new-york-times', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'wired']

for source in english_sources_ids:
    everything = newsapi.get_everything(sources=source,
                                        from_param='2018-09-22',
                                        to='2018-09-29',
                                        page_size=50,
                                        sort_by='popularity')

    for article in everything['articles']:
        if article['content']:
            truncated_content = article['content'].split('\u2026')[0]

        df_articles = df_articles.append({'url': article['url'],
                                          'url_image': article['urlToImage'],
                                          'article': article['title'],
                                          'datetime': article['publishedAt'],
                                          'news_source': article['source']['id'],
                                          'content': truncated_content
                                          }, ignore_index=True)

df_articles.to_json('df_articles.json', orient='records')
print(len(df_articles))
