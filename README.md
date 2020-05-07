
# PDF Builder

[![Open Source Love](https://camo.githubusercontent.com/d41b9884bd102b525c8fb9a8c3c8d3bbed2b67f0/68747470733a2f2f6261646765732e66726170736f66742e636f6d2f6f732f76312f6f70656e2d736f757263652e7376673f763d313033)](https://opensource.org/licenses/MIT)  [![License: MIT](https://camo.githubusercontent.com/3ccf4c50a1576b0dd30b286717451fa56b783512/68747470733a2f2f696d672e736869656c64732e696f2f62616467652f4c6963656e73652d4d49542d79656c6c6f772e737667)](https://opensource.org/licenses/MIT)  [![Actions Status](https://github.com/Samagra-Development/PDF-Package/workflows/Pylint/badge.svg)](https://github.com/Samagra-Development/PDF-Package/actions)  

-   [Overview](https://github.com/Samagra-Development/PDF-Package#overview)
-   [Installation](https://github.com/Samagra-Development/PDF-Package#installation)
-  [Usage](https://github.com/Samagra-Development/PDF-Package#usage)
-   [Contribute](https://github.com/Samagra-Development/PDF-Package#contribute)
-   [License](https://github.com/Samagra-Development/PDF-Package#license)

## [](https://github.com/Samagra-Development/PDF-Package#overview)Overview

PDF Builder is offer a service for governance applications to generate PDF views of the information generated through independent systems to allow users to have access to printable views of the information.

## [](https://github.com/Samagra-Development/PDF-Package#installation)Installation

 - Take Clone of repository
 - From the root folder run the following command
	`pip install -r requirements.txt`
 - [Install postgres](https://www.digitalocean.com/community/tutorials/how-to-install-and-use-postgresql-on-ubuntu-18-04) and add database detail in src/db/config.py
 - Go to folder src/db and run following command database table creation:
		 
	 - Create a migration repository with the following command:
		`FLASK_APP=app.py flask db init`
	 - Generate an initial migration:
		`FLASK_APP=app.py flask db migrate`
	 - Run migration:
		 `FLASK_APP=app.py flask db upgrade` 

 ## [](https://github.com/Samagra-Development/PDF-Package#usage)Usage	 	 
 - To Fetch data from GoogleSheet run the following command from root folder
		`python3 -m src.plugin.GoogleDocPlugin.server`
 - To Fetch data from Form Response run the following command from root folder
		`python3 -m src.plugin.ODKPlugin.server`
 - To generate pdf from request run the following command from root folder
		`python3 -m  src.pdfbase.main`
		
 ## [](https://github.com/Samagra-Development/PDF-Package#contribute)Contribute

Please use the  [issues tracker](https://github.com/Samagra-Development/PDF-Package/issues)  to raise bug reports and feature requests. We'd love to see your pull requests, so send them in!
## [](https://github.com/Samagra-Development/PDF-Package#license)License

```
MIT License

Copyright (c) 2021 Pdf Package

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```