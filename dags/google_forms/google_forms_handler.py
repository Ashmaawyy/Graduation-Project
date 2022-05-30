# pylint: disable=bad-indentation
# pylint: disable=missing-module-docstring
# pylint: disable=anomalous-backslash-in-string
import os
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pandas import read_excel

def access_drive():
	"""
	To access google drive
	"""
	# Initializing a GoogleAuth Object
	gauth = GoogleAuth()

	# client_secrets.json file is verified
	# and it automatically handles authentication
	gauth.LoadCredentialsFile("creds.txt")

	if gauth.credentials is None:
    	# Authenticate if they're not there
		GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = os.getcwd() + '\client_secrets.json'
		gauth.LocalWebserverAuth()
	elif gauth.access_token_expired:
    	# Refresh them if expired
		gauth.Refresh()
	else:
    	# Initialize the saved creds
		gauth.Authorize()

	gauth.SaveCredentialsFile("creds.txt")

	# GoogleDrive Instance is created using authenticated GoogleAuth instance
	drive = GoogleDrive(gauth)
	return drive

def read_form_response():
	"""
	To return a dataframe with the expected google form responces
	"""
	drive = access_drive()
	# Initialize GoogleDriveFile instance with file id
	file_obj = drive.CreateFile({'id': '1B7d0Ds_amgNwf8DjkmKZFQK9RCPn6zNZxQ8W2VnSOz0'})
	file_obj.GetContentFile('Test.xls',
			mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

	form_responces_df = read_excel('Test.xls')
	return form_responces_df
