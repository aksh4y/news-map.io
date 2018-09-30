from flask import Flask, session, request, url_for, redirect, flash, render_template, jsonify
from flask_cors import CORS
from os import environ
import json
from collections import defaultdict
from werkzeug.contrib.cache import SimpleCache
from nytimes_helper import get_nytimes_articles_coordinates, get_dict_to_csv

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
	ret_articles = get_nytimes_articles_coordinates(cache)
	# Provide support for csv if specified
	if 'csv' in request.args:
		ret_articles = get_dict_to_csv(ret_articles)
		return ret_articles
	return jsonify(ret_articles)

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=environ.get('port', 8000))