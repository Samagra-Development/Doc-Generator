



# PDF Builder

[![Open Source Love](https://camo.githubusercontent.com/d41b9884bd102b525c8fb9a8c3c8d3bbed2b67f0/68747470733a2f2f6261646765732e66726170736f66742e636f6d2f6f732f76312f6f70656e2d736f757263652e7376673f763d313033)](https://opensource.org/licenses/MIT)  [![License: MIT](https://camo.githubusercontent.com/3ccf4c50a1576b0dd30b286717451fa56b783512/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)  [![Actions Status](https://github.com/Samagra-Development/PDF-Package/workflows/Pylint/badge.svg)](https://github.com/Samagra-Development/PDF-Package/actions)  

-   [Overview](https://github.com/Samagra-Development/PDF-Package#overview)
-    [Features](https://github.com/Samagra-Development/PDF-Package#features)
-   [Installation](https://github.com/Samagra-Development/PDF-Package#installation)
	-  [Installation Without Docker](https://github.com/Samagra-Development/PDF-Package#installation-without-docker)
	-   [Installation With Docker](https://github.com/Samagra-Development/PDF-Package#installation-with-docker)
-  [Usage](https://github.com/Samagra-Development/PDF-Package#usage)
-   [Contribute](https://github.com/Samagra-Development/PDF-Package#contribute)
-   [License](https://github.com/Samagra-Development/PDF-Package#license)

## [](https://github.com/Samagra-Development/PDF-Package#overview)Overview

PDF Builder is offer a service for governance applications to generate PDF views of the information generated through independent systems to allow users to have access to printable views of the information.
The key aspects of this PDF Builder are summarized below.

1.  PDF Builder is designed to increase the ease of creation of printable PDFs for governance application providers
    
2.  Provides a simple mechanism to map information templates to PDF output designs
    
3.  Supports in facilitating the Digital India vision to develop user centric governance projects
## [](https://github.com/Samagra-Development/PDF-Package#features)Features

PDF Builder has the following features:

1.  Ability to provide a single input request
    
2.  Ability to provide a single custom input request (supplementary feature/block, helper function)
    
3.  Ability to provide a bulk input request
    
4.  Ability to provide a bulk custom input request (custom - supplementary feature, helper function)
    
5.  Ability to review the status of single requests
    
6.  Ability to review the status of bulk requests. Teacher’s were good.

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
 ### [](https://github.com/Samagra-Development/PDF-Package#installation-with-docker) Installation with Docker
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
 - To generate pdf from request, first fetch data from request using above 2 step and then run the following command from root folder
	```shell
	  $ python3 -m pdfbase.main 
	  ```
		
 ## [](https://github.com/Samagra-Development/PDF-Package#contribute)Contribute

> To get started...

### [](https://github.com/Samagra-Development/PDF-Package#step-1)Step 1

-   **Option 1**
    
    -     Fork this repo!
-   **Option 2**
    
    -   Clone this repo to your local machine using  
	    ```shell 
	    https://github.com/Samagra-Development/PDF-Package.git
	    ```

### [](https://github.com/Samagra-Development/PDF-Package#step-2)Step 2

-   From the root folder run the following command
    ```shell
     $ pip install -r requirements.txt
      ``` 

### [](https://github.com/Samagra-Development/PDF-Package#step-3)Step 3

 -   [Install postgres](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) and add database detail in **src/db/config.py**	

### [](https://github.com/Samagra-Development/PDF-Package#step-4)Step 4

-   Go to folder src and run following command database table creation:
    
    -   Create a migration repository with the following command:  
          ```shell 
          $ FLASK_APP=db/app.py flask db init
          ```
    -   Generate an initial migration:  
	      ```shell
	     $ FLASK_APP=db/app.py flask db migrate
	     ```
    -   Run migration:  
          ```shell
           $ FLASK_APP=db/app.py flask db upgrade
           ```  
	
## [](https://github.com/Samagra-Development/PDF-Package#license)License
[![License](https://camo.githubusercontent.com/107590fac8cbd65071396bb4d04040f76cde5bde/687474703a2f2f696d672e736869656c64732e696f2f3a6c6963656e73652d6d69742d626c75652e7376673f7374796c653d666c61742d737175617265)](http://badges.mit-license.org/)

-   **[MIT license](http://opensource.org/licenses/mit-license.php)**
