import os.path

from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from httplib2 import Http
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive']


credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'service_account.json', SCOPES
)
http_auth = credentials.authorize(Http())

drive_service = build('drive', 'v3', http=http_auth)

upload_file_path = "./test.csv"
upload_file_name = os.path.basename(upload_f_path)
mine_type = 'text/csv'
folder_id = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'

media = MediaFileUpload(upload_file_path, mimetype=mine_type, resumable=True)

file_metadata = {
    'name': upload_file_name,
    'mimeType': mine_type,
    'parents': [folder_id]
}
file = drive_service.files().create(
        body=file_metadata, 
        media_body=media 
		    ).execute()

print(file['id'])