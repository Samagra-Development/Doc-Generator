# Installation and Setup

1. Create a Virutal Environment and install the local dependencies `pip install -r requirements.txt`.
2. Setup the PSQL server using the docker-compose.yml file.
3. Update the credentials of PSQL in the config.py file.
4. Setup the Google Credentials for service account credentials on google developer console.
5. Enable the following API => Google Docs, Google Sheets, Google Cloud Storage.
6. Configure consent screen.
7. Creating a Oauth2 access token json from Google developer console.
8. Updating the appa nd instance folder which have the same thing.
9. Setting up Google App Scripts and publishing it as a web app. This will require you to be the admin of the app or it won't work. (See network tab on Google Chrome dev console if you have issues with it)
10. Update the url in Config.py

# Template to PDF

Design Document available at - [https://docs.google.com/document/d/1hA9et-PveVmXZYZ4C3LAj_RfxdGPyRScRK3Aa3GHibY/edit](https://docs.google.com/document/d/1hA9et-PveVmXZYZ4C3LAj_RfxdGPyRScRK3Aa3GHibY/edit)

API Specifications available in the design document.

# Limitations

- No user authentication is available.
- The template document should be available on the authenticated account’s drive. It won’t work if the doc is shared as read/write with the authenticated account.
- If the options are using apostrophe then python and app script aren't parsing it. Eg. Teacher’s were good, is working great. But Teacher's are good, is not working well.
- The image dimensions in app script are fixed 1:1.
- The queue processing part is synchronous. It can be made asynchronous to make it fast OR multithreading can be implemented there.
- Different templates are required for different versions of forms.
- The intermediate google docs are created in the same location as that of template doc.
- If app script failed due to any runtime error then a junk google doc is still created.
- [Custom part] - The distance using udise is not yet calculated.
- Google App script usage limitations (url fetching) (https://developers.google.com/apps-script/guides/services/quotas#current_limitations)

# Monitoring

Below are a few of the things that needs to be continuously monitored, all these can be monitored by creating a testing route which keeps the results of all the following things:

- Is the Data collection API alive? - It can be checked by sending a dummy data.
- Is the check status API alive? - It can be checked by sending a dummy request.
- Is the database working? - It can be checked by sending a count rows query.
- Is the file downloading (from drive) working? - It can be checked by tracking the status of the dummy request sent in point 1.
- Is the file uploading (to google cloud) working? - It can be checked by placing a file in uploadFiles directory and then checking if it is uploaded or not. If would be a success if the file is available at the following url - https://storage.googleapis.com/pdf-generator-1/fileName.pdf
- Total number of failed requests in database? - It can be checked by sending a db query.
- Queue size (unprocessed requests)? - It can be checked by sending a db query.
- Is the data fetching from sheet working? - It can be checked by monitoring the dummy request sent in step 1.
