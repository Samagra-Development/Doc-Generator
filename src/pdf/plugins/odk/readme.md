
---  
id: FormResponses2PDF  
title: Form Response to PDF  
sidebar_label: Form Response to PDF (alpha)  
---  
  
## 1. Overview  
  
Over the past few years, various day to day functions of governments in India are being rapidly digitized. Information generated from these functions is stored online and made available through dashboards to enable data backed decision making within the government. However, traditionally, reviews within the government heavily relied on printed sheets of data rigorously arranged and distributed to every participant.  
  
It is against this backdrop of an evolving ecosystem of data representation for governance decision making that there was a need to bridge the traditional practice of decision making through paper based reviews to a completely online, dashboard driven reviews.  
  
#### TLDR - Key Features  
  
- Convert ODK Form Responses to PDF  
- Convert Google Forms to PDF  
- Make a base project to convert other forms of templated media to PDF, example Markdown, Images, email etc. This can be done through extending the base converter to suit your needs.  
  
## 2. Getting started  
  
### 2.0 Disclaimer  
  
- _Note that this project in alpha and the APIs can change without notice. Please use it at your discretion. Though we use it in production, but the we are yet to close the API specification_  
  
- _This doc assumes you have already done the ODK setup for the the setup_  
  
### 2.1 Setting up the docs and data  
  
The first steps are to create the template and mapping data. The detailed docs to which will be added in following week.  
  
### 2.2 Setting up the google services.  
  
1. Setup the [Google Credentials for service account credentials](https://developers.google.com/identity/protocols/oauth2/service-account) on google developer console .  
2. Copy Service account json credential in google_doc_plugin folder and name it as gcs-creds.json.  
3. [Enable the following API](https://support.google.com/googleapi/answer/6158841?hl=en) => Google Docs, Google Sheets, Google Cloud Storage.  
4. Inside the gcs-creds.json, you can locate an email address property called “client_email”, copy that and take it over to our spreadsheet on the cloud, we can share that particular spreadsheet with the email address present in client_email.  
6. Create a [Google App Script](https://developers.google.com/apps-script/overview#your_first_script) and delete all code and copy code from **google_app_script_code.js** file in google_doc_plugin and paste it on script editor and then publish it as a deploy as web app.Deploy as web app pop up opens and select "**Anyone,Even Anoynmous**" in **Who has access to the app** . (See network tab on Google Chrome dev console if you have issues with it)  
7. Update the url in config.json.  
8. Create [Google Cloud Storage Bucket](https://cloud.google.com/storage/docs/creating-buckets#storage-create-bucket-console) and update the bucket name and GOOGLECLOUDBASEURL in config.json.  
  
### 2.3 Fixing the config file  
  
The config file containes all the credentails and configurations that are required for the plugin to work. A sample config file is show below. Please duplicate this and fill the entried based on whatever you have and remove the documentation (json doesn't allow docstrings)  
  
```json  
{  
  "GOOGLE_APPLICATION_CREDENTIALS": "GoogleDocPlugin/gcs-creds.json", #It contains the path of gcs-creds.json file.  
 "BUCKET": "test",#Google Cloud Storage bucket name  
 "URL": "https://script.google.com/macros/s/AKfycbw1Et6M-NEQ9nnPw5OqSt5kCCFgasdR1dsIZasjkdhak/exec?",#It contains Google App Scripts execution url  
 "GOOGLECLOUDBASEURL": "https://storage.googleapis.com/test/",#It contain google cloud storage base url  
 "DRIVE_DELETE_URL": "https://script.google.com/macros/s/AKfycbw1Et6M-NEQ9nnPw5OqSt5kCCFgasdR1dsIZasjkijhg/exec?",#It contains Google App Scripts execution url for delete file from google drive
 "MAPPINGDETAILS": "mappingDetails",#It contains the sheet name of SHEETID from where mapping detail is fetched. 
 "OPTIONSSHEET": "optionsSheet", #It contains the sheet name of SHEETID from where option detail is fetched. 
 "UPLOADTO" : "google", # It can be aws or google where we want to save file (optional). 
"ODKUSERNAME": "username",  # It contains odk usernmae
"ODKPASSWORD": "password", # It contains odk password
"SESSIONCOOKIEBASEURL": "http://aggregate.cttsamagra.xyz:8080/Aggregate.html#submissions/filter///", #It contains login url for validating odk user
 "DIRPATH": "/../../uploadFiles/", # It contains relative path where created pdf save on local.  "ACCESSKEY": "asfgkasgfka",# access key of aws for saving file on aws server (Required only if we set UPLOADTO with aws). 
 "SECRETKEY": "klfjalfja", #secret key of aws .
 "POLRACCESSTOKEN": "1276847920323562",  # polr access token for generating short url
"POLRAPIURL": "http://68.183.94.187/api/v2/action/shorten", #url of polr api
"resume_questionnaire_v3":{ # form id 
  "APPLICATIONID": "1122",  
  "SHEETID": "14dlQIEo92raBCz26iAzt__duZvdkasjhfkajshfk", #It contains google sheet id from where data and mapping is fetched. 
  "DOCTEMPLATEID": "114TbCy3_QYVGRjGXyj5ac6754fgtyopdrfYT", #It contains template id of pdf that needs to be generated. 
  "FORMNAME": "Resume Questionnaire", # It contains form name 
  "GOOGLE_APPLICATION_CREDENTIALS": "../google_doc_plugin/gcs-creds.json", #It contains path where google credential is save 
  "USERNAMEFIELD": "mobile_number",  #Field name from which we get username
  "SENDMSG": "TRUE",  #It can be TRUE/FALSE true if we want to send whatsapp msg to user
  "SENDEMAIL": "TRUE",#It can be TRUE/FALSE true if we want to send email to user  
  "MSGFIELD": "mobile_number", # Field name from where we get user mobile number  
  "NAMEFIELD": "full_name",  # Field name which contain name of user
  "EMAILFIELD": "email_id", # Field name which contain email of user  
  "EMAILTEMPLATEID": 4, # Template id of email generatedin mailtrain server
  "DOCDELETED": false  #It can be TRUE/FALSE true if we want to delete pdf saved on drive 
},
 }  
```  
  
  
### 2.4 Running the system.  
  
From the root folder run the following command to start converting data to PDF. `python src/pdfbase/main.py`  
  
You should start seeing the PDFs in the `upload` folder.  
  
## 3. Limitations  
  
1. The template document should be available on the **authenticated account’s drive**. It won’t work if the doc is shared as read/write with the authenticated account.  
2. If the options are using **apostrophe** then python and app script aren't parsing it. Eg. Teacher’s were good, is working great. But Teacher**'**s are good, is not working well.  
3. The **image dimensions** in app script are fixed 1:1.  
4. The **intermediate google docs are created** in the same location as that of template doc.  
5. If app script failed due to any runtime error then a **junk google doc is still created**.  
6. Google App script usage limitations (url fetching) ([https://developers.google.com/apps-script/guides/services/quotas#current_limitations](https://developers.google.com/apps-script/guides/services/quotas#current_limitations))  
  
## 4. FAQs  
  
To be added based on incoming feedback  
  
## 5. Coming Soon  
  
- Monitoring setup  
- Single click setup except for the base project  
- FusionAuth integration