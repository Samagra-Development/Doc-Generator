'''Make sure to replace 'path/to/credentials.json' with the actual path to your 
credentials file and provide the appropriate file and folder IDs for the upload, download, and delete operations.'''
# Create an instance of the storage plugin
plugin = GoogleDriveStoragePlugin('path/to/credentials.json')

# Upload a file to Google Drive
plugin.upload_file('path/to/local/file.txt', 'google_drive_folder_id')

# Download a file from Google Drive
plugin.download_file('google_drive_file_id', 'path/to/local/folder')

# Delete a file from Google Drive
plugin.delete_file('google_drive_file_id')
