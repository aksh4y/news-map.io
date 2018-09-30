from os import environ
import requests
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

google_key = environ.get('google_key', '')

GOOGLE_GEOCODE_API = 'https://maps.googleapis.com/maps/api/geocode/json'

def extract_location_from_text(content):
	entities = extract_possible_entities(content)
	return list(map(get_address, entities))
	
def extract_possible_entities(text):
	stop_words = set(stopwords.words('english'))
	print('Before tokenize', len(text))
	word_tokens = word_tokenize(text)
	print('After tokenize')
	current = ''
	entities = []
	for word in word_tokens:
		print('Doing word', word)
		if word.lower() not in stop_words:
			if word.isupper() or word.istitle():
				current += bool(current)*' ' + word
				continue
		if bool(current):
			entities.append(current)
			current = ''
	return entities

def get_address(entity):
	address_results = requests.get(GOOGLE_GEOCODE_API, params={
		'address': entity,
		'key': google_key
		})
	results = address_results.json().get('results', [])
	if len(results) > 0:
		return {
		'address': results[0].get('formatted_address', ''),
		'coordinates': results[0].get('geometry', {}).get('location', {})
		}
	else:
		return None

if __name__ == '__main__':
	from pprint import pprint
	entities = extract_possible_entities('In the late 1990s and early 2000s, there was widespread communal violence in and around Poso, a port city not far from Palu that is mostly Christian. More than 1,000 people were killed and tens of thousands dislocated from their homes as Christian and Muslim gangs battled on the streets, using machetes, bows and arrows, and other crude weapons.')
	for entity in entities:
		pprint(get_address(entity))