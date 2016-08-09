import os, time
from flask import Flask, render_template, session, escape, g, request, url_for, redirect, flash
from boxsdk import OAuth2, Client
from boxsdk.exception import BoxAPIException

import auth

app = Flask(__name__)
app.config.from_object('config')

@app.before_request
def load_auth_obj():
	if "/static/" in request.path:
		return


@app.route('/', methods=['GET', 'POST'])
def index_page():

	if request.method == 'POST':
		client_id = request.form.get('clientID', None)
		client_secret = request.form.get('clientSecret', None)
		access_token= request.form.get('accessToken', None)
		refresh_token = request.form.get('refreshToken', None)
		auth.setCredentials(client_id, client_secret, access_token, refresh_token)
	
	credentials = auth.getCredentialsJSON()

	print credentials
	return render_template("index.html", credentials=credentials)

@app.route('/listusers')
def listusers():
	return render_template("listusers.html")

port=int(os.getenv('PORT', '5000'))
if __name__ == "__main__":
	app.run(host="0.0.0.0", port=port, debug=app.config['DEBUG'])