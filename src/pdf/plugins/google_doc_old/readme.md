
---
id: GoogleDoc2PDF
title: Google Docs to PDF
sidebar_label: Google Docs to PDF
---

## 1. Overview

This plugin is used to convert templated google docs to PDF.

## 2. Getting started

### 2.1 Setting up the docs

The first steps are to create the template and mapping data. The detailed docs to which will be added in following week.

### 2.2 Setting up the google services.

1.  Setup the [Google Credentials for service account credentials](https://developers.google.com/identity/protocols/oauth2/service-account) on google developer console .
2.  Copy Service account json credential in google_doc_plugin folder and name it as gcs-creds.json.
3.  [Enable the following API](https://support.google.com/googleapi/answer/6158841?hl=en) => Google Docs, Google Sheets, Google Cloud Storage.
4. Inside the gcs-creds.json, you can locate an email address property called “client_email”, copy that and take it over to our spreadsheet on the cloud, we can share that particular spreadsheet with the email address present in client_email.
5.  Create a [Google App Script](https://developers.google.com/apps-script/overview#your_first_script) and delete all code and copy code from **google_app_script_code.js** file in google_doc_plugin and paste it on script editor and then publish it as a deploy as web app.Deploy as web app pop up opens and select "**Anyone,Even Anoynmous**" in **Who has access to the app** . (See network tab on Google Chrome dev console if you have issues with it)
6.  Update the url in googledoc-config.json.
7.  Create [Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-console) and update the bucket name and GOOGLECLOUDBASEURL in googledoc-config.json.
8. For Deleting file from google drive
	1. Create a [Google App Script](https://developers.google.com/apps-script/overview#your_first_script) and delete all code and copy code from **google_app_script_delete_file.js** file in google_doc_plugin and paste it on script editor.
	2. Enable Drive Api:
			To enable the Drive API, open the Resources menu, then choose the Advanced Google Services, and a menu will pop up. You need to click the **Drive API** service. Make sure that the green "ON" text is showing
			![Enable Drive Api ](https://i.stack.imgur.com/6vBFU.jpg)
	3.	Then publish it as a deploy as web app.Deploy as web app pop up opens and select "**Anyone,Even Anoynmous**" in **Who has access to the app** .
	4.	Update the DRIVE_DELETE_URL in googledoc-config.json.
	

### 2.3 Fixing the config file

The config file containes all the credentails and configurations that are required for the plugin to work. A sample config file is show below. Please duplicate this and fill the entried based on whatever you have and remove the documentation (json doesn't allow docstrings)

```json
{
  "GOOGLE_APPLICATION_CREDENTIALS": "GoogleDocPlugin/gcs-gdrive_dev_creds.json", #It contains the path of gcs-creds.json file.
  "BUCKET": "test",#Google Cloud Storage bucket name
  "URL": "https://script.google.com/macros/s/AKfycbw1Et6M-NEQ9nnPw5OqSt5kCCFgasdR1dsIZasjkdhak/exec?",#It contains Google App Scripts execution url
  "GOOGLECLOUDBASEURL": "https://storage.googleapis.com/test/",#It contain google cloud storage base url
  "SHEETID":"1_iE1D8Pvsq7SQMMjHashidGvkXENiluq01RXvb3nsdg",# It contains google sheet id from where data and mapping is fetched.
  "SHEETNAME":"PDF generator excel", #It contains the sheet name of the first sheet of SHEETID from where data is fetched.
  "RANGE":"C1:AM37", # Optional Specifies if there is an empty column in the starting of {SHEETNAME}.
  "MAPPINGDETAILS": "mappingDetails",#It contains the sheet name of SHEETID from where mapping detail is fetched.
  "OPTIONSSHEET": "optionsSheet", #It contains the sheet name of SHEETID from where option detail is fetched.
  "DOCTEMPLATEID": "1g7EvvBPsMi2kXyg0am-iRZ72DJNZNtyasdasas",#It contains template id of pdf that needs to be generated.
  "APPLICATIONID":"test", #It contains application id whose pdf is generated.
  "DIRPATH": "/../../uploadFiles/", # It contains relative path where created pdf save on local.
  "UPLOADTO" : "google", # It can be aws or google where we want to save file (optional).
  "ACCESSKEY": "asfgkasgfka",# access key of aws for saving file on aws server (Required only if we set UPLOADTO with aws).
  "SECRETKEY": "klfjalfja" #secret key of aws .
}
```

### 2.4 Running the system.

From the root folder run the following command to start converting data to PDF. `python src/pdfbase/main.py`

## 3. Limitations

1.  The template document should be available on the **authenticated account’s drive**. It won’t work if the doc is shared as read/write with the authenticated account.
2.  If the options are using **apostrophe** then python and app script aren't parsing it. Eg. Teacher’s were good, is working great. But Teacher**'**s are good, is not working well.
3.  The **image dimensions** in app script are fixed 1:1.
4.  The **intermediate google docs are created** in the same location as that of template doc.
5.  If app script failed due to any runtime error then a **junk google doc is still created**.
6.  Google App script usage limitations (url fetching) ([https://developers.google.com/apps-script/guides/services/quotas#current_limitations](https://developers.google.com/apps-script/guides/services/quotas#current_limitations))

## 4. FAQs

To be added based on incoming feedback

## 5. Coming Soon

Please review the following section to get information about planned updates to this module.
