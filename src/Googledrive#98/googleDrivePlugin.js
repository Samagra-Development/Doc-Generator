import { useEffect } from 'react';
import { google } from 'googleapis';

export default function GoogleDrivePlugin() {
  useEffect(() => {
    // Initialize Google Drive API client
    const auth = new google.auth.GoogleAuth({
      keyFile: 'path/to/credentials.json',
      scopes: ['https://www.googleapis.com/auth/drive'],
    });

    const drive = google.drive({ version: 'v3', auth });

    // Example: List files in Google Drive
    const listFiles = async () => {
      try {
        const response = await drive.files.list({
          pageSize: 10,
          fields: 'nextPageToken, files(name, webViewLink)',
        });

        const files = response.data.files;
        if (files.length) {
          console.log('Files in Google Drive:');
          files.forEach((file) => {
            console.log(`${file.name} (${file.webViewLink})`);
          });
        } else {
          console.log('No files found in Google Drive.');
        }
      } catch (error) {
        console.error('Error listing files in Google Drive:', error);
      }
    };

    listFiles();
  }, []);

  return <div>Google Drive Plugin</div>;
}
