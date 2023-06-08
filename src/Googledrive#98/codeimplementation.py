''' To use this plugin, you'll need to create a service account on the Google Cloud Console and download the 
JSON credentials file.  Then, you can create an instance of the GoogleDriveStorage 
Plugin class by providing the path to the credentials file. '''

import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class GoogleDriveStoragePlugin:
    def __init__(self, credentials_file):
        self.credentials_file = credentials_file
        self.service = self._create_drive_service()

    def _create_drive_service(self):
        credentials = service_account.Credentials.from_service_account_file(self.credentials_file, scopes=["https://www.googleapis.com/auth/drive"])
        service = build('drive', 'v3', credentials=credentials)
        return service

    def upload_file(self, local_file_path, drive_folder_id):
        file_name = os.path.basename(local_file_path)
        file_metadata = {
            'name': file_name,
            'parents': [drive_folder_id]
        }
        media = MediaFileUpload(local_file_path)
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
        print(f"File '{file_name}' uploaded successfully. File ID: {file.get('id')}")

    def download_file(self, file_id, destination_folder):
        request = self.service.files().get_media(fileId=file_id)
        file_name = request.execute()["name"]
        file_path = os.path.join(destination_folder, file_name)
        with open(file_path, "wb") as f:
            downloader = request.get_media()
            done = False
            while not done:
                status, done = downloader.next_chunk()
                print(f"Download progress: {status.progress() * 100:.2f}%")
            print(f"File '{file_name}' downloaded successfully to: {file_path}")

    def delete_file(self, file_id):
        self.service.files().delete(fileId=file_id).execute()
        print(f"File with ID: {file_id} deleted successfully")
