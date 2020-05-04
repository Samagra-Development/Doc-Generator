Steps for Extending Plugin

 1. Import Superclass in plugin file.
		E.g 
   from GoogleDocPlugin.external import GoogleDocsSheetsPlugin
    

 2. Create plugin class by extending this superclass.
	E.g 
	    class ODKPlugin(GoogleDocsSheetsPlugin):
 3. All the superclass method are available here. If we need to override the superclass method then we can simply add the method with same name and argument and we can also call superclass method using super statement
  E.g File GoogleDocsPlugin/external.py
 		
 		
		from pdfbase.internal import PDFPlugin
	    from interface import implements
	    class GoogleDocsSheetsPlugin(implements(PDFPlugin)):
	    def __init__(self):
        with open(os.path.dirname(__file__) + '/googledoc-config.json') as json_file: 
            config = json.load(json_file) 
            self.config = config
                       
		def fetch_data(self):
        return mappingValues,tags, error
`
	File ODFPlugin/external.py
	

    from GoogleDocPlugin.external import GoogleDocsSheetsPlugin
	    class ODFPlugin(GoogleDocsSheetsPlugin):
	                   
		def fetch_data(self):
        return mappingValues,tags, error
		def get_mapping_data(self):
			super().fetch_data()`
 
	
	    
﻿
