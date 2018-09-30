from flask import Flask, session, request, url_for, redirect, flash, render_template, jsonify
from flask_cors import CORS
from os import environ
import json
from collections import defaultdict
from werkzeug.contrib.cache import SimpleCache
import nytimes_helper as nyt
import cnn_helper as cnn
import washingtonpost_helper as wapo
import foxnews_helper as fox
from datetime import datetime
import csv

cache = SimpleCache()

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
	return 'hi'

@app.route('/dummydata')
def get_dummy():
	sample_body = {
		'url': 'https://c3c120d4.ngrok.io/deezdata',
		'title': 'Click the link lol',
		'pic': 'https://www.google.com/images/branding/googlelogo/2x/googlelogo_color_272x92dp.png'
	}
	samples = [
		{'address': 'Poso, Sayo, South Poso Kota, Poso Regency, Central Sulawesi, '
	            'Indonesia',
		'coordinates': {'lat': -1.3949976, 'lng': 120.753772}},
		{'address': 'Palu City, Central Sulawesi, Indonesia',
		'coordinates': {'lat': -0.8679099, 'lng': 119.9046594}},
		{'address': '301 S Market St, Tyro, KS 67364, USA',
		'coordinates': {'lat': 37.03381900000001, 'lng': -95.82134429999999}},
		{'address': '301 S Market St, Tyro, KS 67364, USA',
		'coordinates': {'lat': 37.03381900000001, 'lng': -95.82134429999999}},
		{'address': '3020 E 4th Pl, Tulsa, OK 74104, USA',
	 	'coordinates': {'lat': 36.1545263, 'lng': -95.9451897}}
		]

@app.route('/getArticles')
def get_articles():
	start_time = datetime.now()
	nytimes_articles = nyt.get_articles_coordinates(cache)
	cnn_articles = cnn.get_articles_coordinates(cache)
	fox_articles = fox.get_articles_coordinates(cache)
	wapo_articles = wapo.get_articles_coordinates(cache)

	ret_articles = nytimes_articles
	for key in cnn_articles:
		ret_articles.setdefault(key, []).extend(cnn_articles[key])

	for key in fox_articles:
		ret_articles.setdefault(key, []).extend(fox_articles[key])
	
	for key in wapo_articles:
		ret_articles.setdefault(key, []).extend(wapo_articles[key])

	with open('ret_articles.json', 'w') as jsonf:
		json.dump(ret_articles, jsonf)

	# Provide support for csv if specified
	if 'csv' in request.args:
		csv_headers = """lng,lat,url,title,pic,sentiment\n"""
		nytimes_articles = nyt.get_dict_to_csv(nytimes_articles)
		cnn_articles = cnn.get_dict_to_csv(cnn_articles)
		fox_articles = fox.get_dict_to_csv(fox_articles)
		wapo_articles = wapo.get_dict_to_csv(wapo_articles)
		print('Article retrieval took:', (datetime.now()-start_time).total_seconds(), 'seconds')
		with open('articles.csv', 'w', newline='\n') as csvf:
			csvf.write(csv_headers)
			csvf.write(nytimes_articles)
			csvf.write(cnn_articles)
			csvf.write(fox_articles)
			csvf.write(wapo_articles)
		return csv_headers + '\n'.join([nytimes_articles, cnn_articles, fox_articles, wapo_articles])
	return jsonify(ret_articles)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=environ.get('port', 8000))