from flask import Flask, session, request, url_for, redirect, flash, render_template
from os import environ

app = Flask(__name__)

@app.route('/')
def index():
	return 'hi'

if __name__ == '__main__':
	app.run(debug=True, host='0.0.0.0', port=environ.get('port', 8000))