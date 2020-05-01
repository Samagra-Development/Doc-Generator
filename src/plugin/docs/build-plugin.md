
Steps for building plugin 
1.  Implements PdfPlugin Interface
E.g
GoogleDocPlugin/external.py file

```
from pdfbase.internal import PDFPlugin
from interface import implements
class GoogleDocsSheetsPlugin(implements(PDFPlugin)):
```


 
Code of pdfbase/internal.py file
 
	  class PDFPlugin(Interface): 
    #FetchData.process() -> Dict  => Fetches "new" data from the database/server/websocket whatever and provides it in the form of dictionary, one PDF at a time.
    #FetchMapping.process() -> Dict => Feches mapping and yeilds it in the form of dictionary
    #BuildPDF.process() -> File => Function to build PDF and return a file
    #UploadPDF.process(key, File) ->  => Fuction to save PDF
    #RetrievePDF.process(key) -> File => Function to get the previously saved PDF from the key

    def fetch_data(self):
        pass

    def fetch_mapping(self,data):
        pass

    def build_PDF(self,raw_data,file_name):
        pass

    def upload_PDF(self,key, file):
        pass

    def retrieve_PDF(self, key):
        pass`
   
    
2.  Define Body of Following function:
	 1.  fetch_data: this will fetch new data from webserver and provide this data as dictionary and also combine configuration data and also provide tags if any.
    2.  fetch_mapping: This will fetch value mapping and options mapping and combine this with data fetch dictionary and return this complete dictionary.
    3.  build_PDF: It will take raw_data and file_name of pdf as input and return filename and pdfUrl.
    4.  upload_PDF: This will upload pdf to server or to any other storage and return its filename.
    5.  retrieve_PDF: This will take pdf name as input and return pdf content.
3. If we need to add more function in class which needs to be accessible from pdfbase class then they should be first define in PDFPlugin interface.
    
 E.g

    from pdfbase.internal import PDFPlugin
	from interface import implements
	class GoogleDocsSheetsPlugin(implements(PDFPlugin)):

    def __init__(self):
        with open(os.path.dirname(__file__) + '/googledoc-config.json') as json_file: 
            config = json.load(json_file) 
            self.config = config
    def fetch_data(self):
        #code for fetching data from sheet and add tags
        return mappingValues,tags, error

    def fetch_mapping(self,data):
        #return rawData which include mapping values and options values and passed data
        return rawData, error
    def build_PDF(self,raw_data,file_name):
        #build pdf using googleapp script
        return fileName,error,pdfUrl                    
                
    def upload_PDF(self, key,file):
        #upload pdf to local server
        return key,error              
        

    def retrieve_PDF(self, key):
	    #return pdf data
        return filedata,error    
        

Steps For Adding this plugin in main file

 1. Import PDFBuilder Class
 
 E.g

	 `from internal import PDFBuilder, PDFPlugin`
 2. Import Plugin File
 
E.g
	`from GoogleDocPlugin.external import GoogleDocsSheetsPlugin`

 3. Add this class as plugin of PdfBuilder class and also pass config if we need any
 
E.g 
  ```
config = {"retries": 1, "max_concurrency": 2}

app =PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=config)
```

 4. Now call run method of PDFBuilder
 
E.g 
`app.run()`

Now main.py will look like :

```
from .internal import PDFBuilder, PDFPlugin
from plugin.GoogleDocPlugin.external import GoogleDocsSheetsPlugin

if __name__ == "__main__":
    config = {"retries": 1, "max_concurrency": 2}
    app = PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=config)
    app.run()	
```
