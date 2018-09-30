import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 \
import Features, KeywordsOptions
import os

natural_language_understanding = NaturalLanguageUnderstandingV1(
  username=os.environ['watson_username'],
  password=os.environ['watson_password'],
  version='2018-03-16')

def get_sentiment(url):
  keywords = natural_language_understanding.analyze(
    url=url,
    features=Features(
      keywords=KeywordsOptions(
        sentiment=True,
        limit=200))).get_result()['keywords']

  sentiment = 0
  relevance = 0
  for keyword_dict in keywords:
      print(keyword_dict)
      try:
        keyword_relevance = keyword_dict['relevance']**(2)
        sentiment += (keyword_dict['sentiment']['score'] * keyword_relevance)
        relevance += keyword_relevance
      except:
        continue

      # print(keyword_dict['relevance'], '\t', keyword_dict['sentiment']['score'], '\t', keyword_dict['text'])
  if relevance == 0:
    return 0
  return sentiment/relevance


if __name__ == '__main__':
  url = 'https://www.usatoday.com/story/tech/talkingtech/2018/02/19/erica-humanoid-robot-chatty-but-still-has-lot-learn/352281002/'
  sentiment = get_sentiment(url)
  print(sentiment)
