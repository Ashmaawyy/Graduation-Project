from os import getcwd
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pandas import read_excel

def get_form_response_df():
	"""
	Returns a dataframe with the expected google form responces.
	
	Renaming questions dictionary:
	'How would you rate the overall learning journey for this course?': 'learning journey',
	'How would you rate the course content in sight of the current market requirements?': 'course content',
	'How would you rate the practical implementation of this course contents?': 'practical implementation',
	'How did this course improve your skill set?': 'skill set improvement',
	"How many new skills did you acquire during the course's journey?": 'new skills acquired'

	"""
	student_survey_questions_rename_dict = {
		'How would you rate the overall learning journey for this course?': 'learning journey',
		'How would you rate the course content in sight of the current market requirements?': 'course content',
		'How would you rate the practical implementation of this course contents?': 'practical implementation',
		'How did this course improve your skill set?': 'skill set improvement',
		"How many new skills did you acquire during the course's journey?": 'new skills acquired'
	}
	drive = get_drive_access()
	file_id = '1UvWmhv59BSTwQMBAaKFFiZM6VRmT6hcrLVYkUwj-k8E'
	file_name = 'Student Survey (Responces).xls'
	get_responces_file(drive, file_id, file_name)
	form_responces_df = read_excel(file_name)
	return form_responces_df.rename(columns = student_survey_questions_rename_dict)

def get_responces_file(drive: GoogleDrive, file_id: str, file_name: str):
	# Initialize GoogleDriveFile instance with file id
	file_obj = drive.CreateFile({'id': file_id})
	file_obj.GetContentFile(
		file_name,
		mimetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

def get_drive_access():
	"""
	gives access to the system's google drive, returns a GoogleDrive instance

	"""
	# Initializing a GoogleAuth Object
	gauth = GoogleAuth()

	# client_secrets.json file is verified
	# and it automatically handles authentication
	gauth.LoadCredentialsFile("creds.txt")

	if gauth.credentials is None:
    	# Authenticate if they're not there
		GoogleAuth.DEFAULT_SETTINGS['client_config_file'] = getcwd() + '/dags/google_forms/client_secrets.json'
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
