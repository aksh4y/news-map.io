from newsapi import NewsApiClient
import pandas as pd

df_articles = pd.DataFrame(data={'url': [],
                                 'article': [],
                                 'datetime': [],
                                 'news_source': []
                                 })

df_locations = pd.DataFrame(data={'location': [],
                                  'latitude': [],
                                  'longitude': []
                                  })

df_articles_locations = pd.DataFrame(data={'url': [],
                                           'location': []
                                           })

newsapi = NewsApiClient(api_key='e9c060f2e421497dbb5e6218b18b4b50')
sources = newsapi.get_sources(language='en')

english_sources_ids = ['abc-news', 'al-jazeera-english', 'associated-press', 'bbc-news', 'bloomberg', 'business-insider', 'buzzfeed', 'cbs-news', 'cnn', 'engadget', 'financial-times', 'fortune', 'fox-news', 'google-news', 'hacker-news', 'independent', 'msnbc', 'national-geographic', 'nbc-news', 'new-york-magazine', 'nhl-news', 'reuters', 'techcrunch', 'techradar', 'the-economist', 'the-guardian-uk', 'the-huffington-post', 'the-new-york-times', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'time', 'usa-today', 'wired']

for source in english_sources_ids:
    everything = newsapi.get_everything(sources=source,
                                        from_param='2018-09-22',
                                        to='2018-09-29',
                                        page_size=50,
                                        sort_by='popularity')

    for article in everything['articles']:
        df_articles = df_articles.append({'url': article['url'],
                                          'article': article['title'],
                                          'datetime': article['publishedAt'],
                                          'news_source': article['source']['id']
                                          }, ignore_index=True)

df_articles.to_json('df_articles.json')
print(len(df_articles))
