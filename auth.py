import os, sys, time, io, json, logging, csv, datetime
from ConfigParser import SafeConfigParser
from boxsdk import OAuth2, Client


configfile_name = "boxconfig.yaml"



def store_tokens(access_t, refresh_t):
	config = SafeConfigParser()
	config.read(configfile_name)

	config.set('boxCredentials', 'accessToken', access_t)
	config.set('boxCredentials', 'refreshToken', refresh_t)
	
	with open(configfile_name, 'w') as f:
		config.write(f)
	return


def testAndUpdateCredentials():
	config = SafeConfigParser()
	config.read(configfile_name)

	client_id = config.get('boxCredentials', 'clientID')
	client_secret = config.get('boxCredentials', 'clientSecret')
	access_token = config.get('boxCredentials', 'accessToken')
	refresh_token = config.get('boxCredentials', 'refreshToken')

	oauth = OAuth2(client_id=client_id, client_secret=client_secret, access_token=access_token, refresh_token=refresh_token, store_tokens=store_tokens)
	client = Client(oauth)

	me = client.user(user_id='me').get()

	config.read(configfile_name)

	return config


def getCredentials():
	if not os.path.isfile(configfile_name):
		print "Credentials not found"
		return None
	else:
		config = testAndUpdateCredentials()
		return config


def getCredentialsJSON():
	if not os.path.isfile(configfile_name):
		print "Credentials not found"
		return None
	else:
		config = testAndUpdateCredentials()

		credentials = {"clientID": config.get('boxCredentials', 'clientID'),
				"clientSecret": config.get('boxCredentials', 'clientSecret'),
				"accessToken": config.get('boxCredentials', 'accessToken'),
				"refreshToken": config.get('boxCredentials', 'refreshToken')}

		return credentials


def setCredentials(client_id, client_secret, access_token, refresh_token):
	config = SafeConfigParser()

	config.add_section('boxCredentials')
	config.set('boxCredentials', 'clientID', client_id)
	config.set('boxCredentials', 'clientSecret', client_secret)
	config.set('boxCredentials', 'accessToken', access_token)
	config.set('boxCredentials', 'refreshToken', refresh_token)
	with open(configfile_name, 'w') as f:
		config.write(f)

	config = testAndUpdateCredentials()

	return config


