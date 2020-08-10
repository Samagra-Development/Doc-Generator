
  
  
  
  
  
# PDF Builder  
  
[![Open Source Love](https://camo.githubusercontent.com/d41b9884bd102b525c8fb9a8c3c8d3bbed2b67f0/68747470733a2f2f6261646765732e66726170736f66742e636f6d2f6f732f76312f6f70656e2d736f757263652e7376673f763d313033)](https://opensource.org/licenses/MIT)  [![License: MIT](https://camo.githubusercontent.com/3ccf4c50a1576b0dd30b286717451fa56b783512/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)  [![Actions Status](https://github.com/Samagra-Development/PDF-Package/workflows/Pylint/badge.svg)](https://github.com/Samagra-Development/PDF-Package/actions)    
  
 - [Overview](https://github.com/Samagra-Development/PDF-Package#overview)  
 - [Features](https://github.com/Samagra-Development/PDF-Package#features)  
 - [Installation](https://github.com/Samagra-Development/PDF-Package#installation)  
 - [Installation Without Docker](https://github.com/Samagra-Development/PDF-Package#installation-without-docker)  
 - [Installation With Docker](https://github.com/Samagra-Development/PDF-Package#installation-with-docker)  
 - [Usage](https://github.com/Samagra-Development/PDF-Package#usage)  
 - [API](https://github.com/Samagra-Development/PDF-Package#api)  
 - [Contribute](https://github.com/Samagra-Development/PDF-Package#contribute)  
 - [License](https://github.com/Samagra-Development/PDF-Package#license)  
  
## [](https://github.com/Samagra-Development/PDF-Package#overview)Overview  
  
PDF Builder is offer a service for governance applications to generate PDF views of the information generated through independent systems to allow users to have access to printable views of the information.  
The key aspects of this PDF Builder are summarized below.  
  
 - PDF Builder is designed to increase the ease of creation of printable PDFs for governance application providers  
      
 - Provides a simple mechanism to map information templates to PDF output designs  
      
 - Supports in facilitating the Digital India vision to develop user centric governance projects  
## [](https://github.com/Samagra-Development/PDF-Package#features)Features  
  
PDF Builder has the following features:  
  
 - Ability to provide a single input request  
      
 - Ability to provide a single custom input request (supplementary feature/block, helper function)  
      
 - Ability to provide a bulk input request  
      
 - Ability to provide a bulk custom input request (custom - supplementary feature, helper function)  
      
 - Ability to review the status of single requests  
      
 - Ability to review the status of bulk requests. Teacher’s were good.  
  
## [](https://github.com/Samagra-Development/PDF-Package#installation)Installation  
  
  
 ### [](https://github.com/Samagra-Development/PDF-Package#installation-without-docker) Installation without Docker 
 -   **Option 1**  
        -     Fork this repo!  
 -   **Option 2**  
     -     Clone this repo to your local machine using  `https://github.com/Samagra-Development/PDF-Package.git`  
 - From the root folder run the following command  
   ```shell  
	 $  pip install -r requirements.txt
	  ```
 - [Install postgres](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) and add database detail in **src/db/config.py**  
 - Go to folder src and run following command database table creation:  
         
 - Create a migration repository with the following command:  
      ```shell  
	 $ FLASK_APP=db/app.py flask db init
	  ```
 - Generate an initial migration:  
      ```shell  
	 $ FLASK_APP=db/app.py flask db migrate     
	  ```  
 - Run migration:  
      ```shell  
	 $ FLASK_APP=db/app.py flask db upgrade 
	 ```  
 - Setup Kafka and add its detail in variable **KAFKA_CREDENTIAL** in src/pdfbase/config.py.	 
	 - KAFKA_CREDENTIAL config variable detail:
	 ```json
		 {
		 'topic': 'topicname',  
	     'bootstrap_servers': ['moped-01.srvs.cloudkafka.com:9094',  
	                           'moped-02.srvs.cloudkafka.com:9094',  
	                           'moped-03.srvs.cloudkafka.com:9094'],  
	     'security_protocol': 'SASL_SSL',  
	     'sasl_mechanism': 'SCRAM-SHA-256',  
	     'sasl_plain_username': 'username',  
	     'sasl_plain_password': 'password',  
	     'group_id': 'form-group',  
	     'auto_offset_reset': 'earliest',
	     'enable_auto_commit': True,  
	     'auto_commit_interval_ms': 1000  
	  }
	```
	 - Data send to kafka is in byte format convert data from json into byte format using
		 ```shell
		 value_bytes = bytes(value, encoding='utf-8')
		 ```
	- E.g of json data
		```json
		{'reqd_data':  
		{
		'req_data':{form_data_json},
		generated_data
		}
		}
		```
		form_data_json:
		```json
		{'*meta-instance-id*': 'uuid:dc364815-28e9-4735-91fb-587c9e03dc7d',  
	  '*meta-model-version*': '7',  
	  '*meta-ui-version*': '-',  
	  '*meta-submission-date*': '2020-07-13',  
	  '*meta-is-complete*': 'True',  
	  '*meta-date-marked-as-complete*': '2020-07-13T03:32:26.335Z',  
	  'form_intro': '-',  
	  'full_name': 'Vikas',  
	  'mobile_number': '9588528178',  
	  'email_id': 'Kumarv96998@gmail.com',  
	  'address_name': 'V. P. O DEVSAR DISTT.& TEH BHIWANI HARYANA - 127021',  
	  'objective_name': 'Secure a responsible career opportunity to fully utilize my training and skills',  
	  'diploma_education_details_intro': '-',  
	  'iti_name': 'Government ITI, Rawaldhi',  
	  'iti_trade_name': 'Mechanic Diesel Engine',  
	  'check_if_class_twelve': 'no',  
	  'class_twelve_details_intro': '-',  
	  'class_twelve_school_name': '-',  
	  'class_twelve_year': '-',  
	  'class_12_stream': '-',  
	  'class_twelve_percentage': '-',  
	  'class_ten_details_intro': '-',  
	  'class_ten_school_name': 'Government Senior Secondary School, Devsar',  
	  'class_ten_year': '2014',  
	  'class_ten_percentage': '55.2',  
	  'experience_details_details_intro': '-',  
	  'experience_details_industry_partner': 'Om Diesel Pvt. Ltd.',  
	  'training_duration': '3',  
	  'achievements_intro': '-',  
	  'achievement_1': '1 Computer',  
	  'achievement_2': '2 participate in academic Boxing tournament',  
	  'skills_intro': '-',  
	  'skill_1': '1 Engine service',  
	  'skill_2': '2 Kirloskar service',  
	  'skil_3': '3 JCB gearbox service',  
	  'skill_4': '4 installation',  
	  'extra_intro': '-',  
	  'extra_curricular_activity_1': '1 SPORTS',  
	  'extra_curricular_activity_2': '2 music',  
	  'place_filling_form': 'Bhiwani',  
	  'candidate_img': 'https://filemanager.gupshup.io/fm/wamedia/demobot1/bb113403-d8bf-4a04-9390-3d51d5bd448c',  
	  'submit_intro': 'Ok',  
	  'instanceID': 'uuid:dc364815-28e9-4735-91fb-587c9e03dc7d',  
	  'calculated_distance': 'Not available'
	  }
		```
	generated_data:
	```json
	'FORMID': 'resume_questionnaire_v3',   
	'INSTANCEID': 'uuid:dc364815-28e9-4735-91fb-587c9e03dc7d',   
	'USERNAME': '9588528178',   
	'FORMSUBMISSIONDATE': '2020-07-13',   
	'GOOGLE_APPLICATION_CREDENTIALS': 'gcs-creds.json',   
	'BUCKET': 'pdf-builder-samagra',   
	'URL': 'https://script.google.com/macros/s/AKfycbwb1faZ6G7oNikT867oi3C-LbEjEcAYmO-N1UjXByxhs_w48xE/exec?',   
	'DRIVE_DELETE_URL': 'https://script.google.com/macros/s/AKfycbyiH-KvXYFg6L2DJXSiv9TQYkN5AiAn1V1ZLJm6YSEndXQo28EB/exec?',   
	'GOOGLECLOUDBASEURL': 'https://storage.googleapis.com/pdf-builder-samagra/',   
	'MAPPINGDETAILS': 'mappingDetails',   
	'OPTIONSSHEET': 'OptionsSheet',   
	'UPLOADTO': 'google',  
	'ODKUSERNAME': 'samagra',   
	'ODKPASSWORD': 'impact@scale',   
	'SESSIONCOOKIEBASEURL': 'http://aggregate.cttsamagra.xyz:8080/Aggregate.html#submissions/filter///',  
	'DIRPATH': '/../../uploadFiles/',   
	'ACCESSKEY': 'AKIAJURL6U4OVX4JCMTA',  
	'SECRETKEY': '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',   
	'SHEETID': '14dlQIEo92raBCz26iAzt__duZvdklJr3pmqUewnPKjw',  
	'DOCTEMPLATEID': '114TbCy3_QYVGRjGXyj5ac7vrM7Wv75QYGJLDmmAiAlo',   
	'BITLYACCESSTOKEN': '171b3760ab9461061eb524035709984160864c72',   
	'POLRACCESSTOKEN': '41873090067550beb0fbd787138e35',  
	'POLRAPIURL': 'http://68.183.94.187/api/v2/action/shorten',   
	'resume_questionnaire_v3': {  
	  'APPLICATIONID': '1122',   
	  'SHEETID': '14dlQIEo92raBCz26iAzt__duZvdklJr3pmqUewnPKjw',   
	  'DOCTEMPLATEID': '114TbCy3_QYVGRjGXyj5ac7vrM7Wv75QYGJLDmmAiAlo',   
	  'FORMNAME': 'Resume Questionnaire',   
	  'GOOGLE_APPLICATION_CREDENTIALS': '../google_doc_plugin/gcs-creds.json',  
	  'USERNAMEFIELD': 'mobile_number',   
	  'SENDMSG': 'TRUE',   
	  'SENDEMAIL': 'TRUE',   
	  'MSGFIELD': 'mobile_number',   
	  'NAMEFIELD': 'full_name',   
	  'EMAILFIELD': 'email_id',   
	  'EMAILTEMPLATEID': 4,   
	  'DOCDELETED': False  
	},  
	'elem_men_v1': {  
	  'APPLICATIONID': '1122',   
	  'SHEETID': '1JrxOXyjIla7mN-01dH5aHBPQ6MAOmcGEkStRV3b32PA',   
	  'DOCTEMPLATEID': '1Zsi2bj8P8oL0RA7HvqG3gYmTM3596k0Er7AVW2qo2zI',   
	  'FORMNAME': 'ELEMENTARY MENTOR VISIT REPORT',   
	  'GOOGLE_APPLICATION_CREDENTIALS': '../google_doc_plugin/gcs-creds.json',  
	  'USERNAMEFIELD': 'user_name'  
	},  
	'tags': {'FORMID': 'resume_questionnaire_v3',   
	  'USERNAME': '9588528178',   
	  'FORMSUBMISSIONDATE': '2020-07-13',   
	  'INSTANCEID': 'uuid:dc364815-28e9-4735-91fb-587c9e03dc7d',   
	  'FORMNAME': 'Resume Questionnaire'  
	},   
	'instance_id': 'uuid:dc364815-28e9-4735-91fb-587c9e03dc7d',  
	'is_delete': False
	```

### [](https://github.com/Samagra-Development/PDF-Package#installation-with-docker) Installation with Docker  
 - Setup Kafka and add its detail in variable **KAFKA_CREDENTIAL** in src/pdfbase/config.py.
 - Go to the project root folder and run following command  
     ```shell  
	 $ docker-compose up --build     
	 ```     
 ## [](https://github.com/Samagra-Development/PDF-Package#usage)Usage        
- To fetch data from google sheet configure google_doc_plugin configuration using [google-doc plugin readme file](https://github.com/Samagra-Development/PDF-Package/tree/master/src/plugin/google_doc_plugin)  and then run following command from root folder  
     ```shell  
	$ python3 -m plugin.google_doc_plugin.server     
	 ```  
 - To fetch data from Form Response configure odk_plugin configuration using [odk plugin readme file]([https://github.com/Samagra-Development/PDF-Package/tree/master/src/plugin/odk_plugin](https://github.com/Samagra-Development/PDF-Package/tree/master/src/plugin/odk_plugin)  and then run following command from root folder  
     ```shell  
	 $ python3 -m plugin.odk_plugin.server    
	  ```    
- Get data from Kafka by run following command
	 ```shell  
	 $ python3 -m pdfbase.data_consumer    
	```        
- To generate pdf from request, first fetch data from request using above 2 step and then run the following command from root folder  
   ```shell  
	$ python3 -m pdfbase.main     
	 ```  
## [](https://github.com/Samagra-Development/PDF-Package#api)API         
 - **Pdf generated for particular user**  
  - This api return all the pdf url with status for particular user. You can find api detail in  [postman collection link](https://www.getpostman.com/collections/18c5019dfecf21bf0214)  
        
 ## [](https://github.com/Samagra-Development/PDF-Package#contribute)Contribute  
  
> To get started...  
  
### [](https://github.com/Samagra-Development/PDF-Package#step-1)Step 1  
  
-   **Option 1**  
     -     Fork this repo!  
-   **Option 2**  
	 - Clone this repo to your local machine using    
       ```shell   
	    https://github.com/Samagra-Development/PDF-Package.git  
		```  
### [](https://github.com/Samagra-Development/PDF-Package#step-2)Step 2  
  
- From the root folder run the following command  
    ```shell  
	$ pip install -r requirements.txt 
	```   
### [](https://github.com/Samagra-Development/PDF-Package#step-3)Step 3  
  
 - [Install postgres](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) and add database detail in **src/db/config.py**   
### [](https://github.com/Samagra-Development/PDF-Package#step-4)Step 4  
  
- Go to folder src and run following command database table creation:  
      
    - Create a migration repository with the following command:    
	    ```shell  
		 $ FLASK_APP=db/app.py flask db init
	  ```  
	 - Generate an initial migration:    
	      ```shell  
		 $ FLASK_APP=db/app.py flask db migrate 
		 ```  
	 - Run migration:    
	      ```shell  
		$ FLASK_APP=db/app.py flask db upgrade 
		 ``` 
 ## [](https://github.com/Samagra-Development/PDF-Package#license)License  
[![License](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)](http://badges.mit-license.org/)  
  
-   **[MIT license](http://opensource.org/licenses/mit-license.php)**