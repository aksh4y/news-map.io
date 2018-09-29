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

english_sources_ids = ['abc-news', 'abc-news-au', 'al-jazeera-english', 'ars-technica', 'associated-press', 'australian-financial-review', 'axios', 'bbc-news', 'bbc-sport', 'bleacher-report', 'bloomberg', 'breitbart-news', 'business-insider', 'business-insider-uk', 'buzzfeed', 'cbc-news', 'cbs-news', 'cnbc', 'cnn', 'crypto-coins-news', 'daily-mail', 'engadget', 'entertainment-weekly', 'espn', 'espn-cric-info', 'financial-post', 'financial-times', 'football-italia', 'fortune', 'four-four-two', 'fox-news', 'fox-sports', 'google-news', 'google-news-au', 'google-news-ca', 'google-news-in', 'google-news-uk', 'hacker-news', 'ign', 'independent', 'mashable', 'medical-news-today', 'metro', 'mirror', 'msnbc', 'mtv-news', 'mtv-news-uk', 'national-geographic', 'national-review', 'nbc-news', 'news24', 'new-scientist', 'news-com-au', 'newsweek', 'new-york-magazine', 'next-big-future', 'nfl-news', 'nhl-news', 'politico', 'polygon', 'recode', 'reuters', 'rte', 'talksport', 'techcrunch', 'techradar', 'the-american-conservative', 'the-economist', 'the-globe-and-mail', 'the-guardian-au', 'the-guardian-uk', 'the-hill', 'the-hindu', 'the-huffington-post', 'the-irish-times', 'the-jerusalem-post', 'the-new-york-times', 'the-next-web', 'the-sport-bible', 'the-telegraph', 'the-times-of-india', 'the-verge', 'the-wall-street-journal', 'the-washington-post', 'the-washington-times', 'time', 'usa-today', 'vice-news', 'wired']

everything = newsapi.get_everything(sources=','.join(english_sources_ids),
                                    from_param='2018-09-22',
                                    to='2018-09-29')
# print(everything['totalResults'])

# print(everything['articles'][0])

for article in everything['articles'][:1000]:
    df_articles = df_articles.append({'url': article['url'],
                                      'article': article['title'],
                                      'datetime': article['publishedAt'],
                                      'news_source': article['source']['id']
                                      }, ignore_index=True)

# print(df_articles.head())

# df_articles.to_json('df_articles.json')
print(len(df_articles))


df_articles.to_parquet('df_articles.parquet.gzip', compression='gzip')
df_locations.to_parquet('df_locations.parquet.gzip', compression='gzip')
df_articles_locations.to_parquet('df_articles_locations.parquet.gzip', compression='gzip')
