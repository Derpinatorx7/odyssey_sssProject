import os
import sys
print('if you didn\'t go to https://developers.google.com/drive/api/v3/quickstart/python and followed step 1, please do it now.')
if 'google-api-python-client oauth2client' not in sys.modules:
	os.system('pip install --upgrade google-api-python-client oauth2client')
from apiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
try:
	import argparse
	flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
	flags = None

SCOPES = 'https://www.googleapis.com/auth/drive.file'
store = file.Storage('storage.json')
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', scope = SCOPES)
    creds = tools.run_flow(flow, store, flags) \
    	if flags else tools.run(flow, store)
DRIVE = build('drive', 'v3', http = creds.authorize(Http()))

def upload_to_drive(FILES #example: ('mmmm.zip', None),('mmmm.txt', 'application/vnd.google-apps.document'),)
	):
	id_list=[]
	global SCOPES,store,creds, DRIVE, flow
	for filename, mimeType in FILES:
		metadata = {'name' : filename}
		if mimeType:
			metadata[mimeType] = mimeType
		res = DRIVE.files().create(body = metadata, media_body = filename).execute()
		if res:
			print('uploaded "{}" ({}) \nId is  {}'.format(filename, res['mimeType'], res.get('id')))
			id_list.append(res.get('id'))
	return id_list



#################################################################################################

def callback(request_id, response, exception):
	if exception:
		print(exception)
	else:
		print('Permission Id: {}'.format(response.get('id')))

def share(mail_list, id_list):
	for file_id in id_list:
		for mail in mail_list:
			batch = DRIVE.new_batch_http_request(callback=callback)
			user_permission = {
				'type': 'user',
				'role': 'writer',
				'emailAddress': mail
			}
			batch.add(DRIVE.permissions().create(
					fileId=file_id,
					body=user_permission,
					fields='id',
			))
			batch.execute()

def DeleteByFileId(file_id):
	try:
		DRIVE.files().delete(fileId=file_id).execute()
	except Exception as error:
		print("an error occured: {}".format(error))
