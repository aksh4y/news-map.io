from os import environ
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

google_key = environ.get('google_key', '')

GOOGLE_GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json'

count = 0
total = 0
def insert_location_into_articles(articles, cache):
	for article in articles:
		article['location'] = extract_location_from_text(article['content'], cache)
	return articles

def extract_location_from_text(content, cache):
	global count, total
	entities = set(extract_possible_entities(content))
	print('Mapping addresses to entities now')
	# print(len(entities), 'entities')
	count = 0
	total = len(entities)
	return list(map(lambda ent: get_address(ent, cache), entities))
	
def extract_possible_entities(text):
	stop_words = set(stopwords.words('english'))
	# print('Before tokenize', len(text))
	word_tokens = word_tokenize(text)
	# print('After tokenize')
	current = ''
	entities = []
	for word in word_tokens:
		print('Evaluating word', word)
		if word.lower() not in stop_words:
			if word.isupper() or word.istitle():
				current += bool(current)*' ' + word
				continue
		if bool(current):
			entities.append(current)
			current = ''
	return entities

def get_address(entity, cache):
	global count
	# print(entity)
	# print('{}/{}'.format(count, total))
	if cache.get('entity'):
		# print('Hit!')
		return cache.get(entity)
	address_results = requests.get(GOOGLE_GEOCODE_API, params={
		'address': entity,
		'key': google_key
		})
	results = address_results.json().get('results', [])
	count += 1
	if len(results) > 0:
		result = {
			'address': results[0].get('formatted_address', ''),
			'coordinates': results[0].get('geometry', {}).get('location', {})
		}
		cache.set(entity, result)
		return result
	else:
		return None

if __name__ == '__main__':
	from pprint import pprint
	
	# entities = extract_possible_entities('In the late 1990s and early 2000s, there was widespread communal violence in and around Poso, a port city not far from Palu that is mostly Christian. More than 1,000 people were killed and tens of thousands dislocated from their homes as Christian and Muslim gangs battled on the streets, using machetes, bows and arrows, and other crude weapons.')
	# for entity in entities:
	# 	pprint(get_address(entity))