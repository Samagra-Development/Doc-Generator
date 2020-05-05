---
id: PDFBuildAPlugin
title: Building A Plugin
sidebar_label: Building A Plugin
---

## 1. Overview

We have defined what a plugin is [here](bla). Every now and then, you would feel the need to either build a plugin, extend a plugin or fix a broken plugin. To be able to do that, you need to have a very basic understanding of how a plugin works and what is the structure described in the following sections. If you want to look at the architecture of the whole thing first to get a bigger picture, please go [here](bla).

## 2. Building your own plugin from scratch

### 2.1 Building the actual plugin

- All plugins implements `PDFPlugin` interface For example take a look at the source code of [google_doc_plugin/external.py](https://github.com/ChakshuGautam/PDF-Package/blob/master/src/plugin/google_doc_plugin/external.py) and see line number 16

```python
class GoogleDocsSheetsPlugin(implements(PDFPlugin)):
```

So what is a `PDFPlugin`? It looks something like this.

```python
class PDFPlugin(Interface):
    def fetch_data(self):
        pass

    def fetch_mapping(self,data):
        pass

    def build_PDF(self,raw_data,file_name):
        pass

    def upload_PDF(self,key, file):
        pass

    def retrieve_PDF(self, key):
        pass
```

- Define Body of Following function: 1. **_fetch_data_**: this will fetch new data from webserver and provide this data as dictionary and also combine configuration data and also provide tags if any.
  2.  **_fetch_mapping_**: This will fetch value mapping and options mapping and combine this with data fetch dictionary and return this complete dictionary.
  3.  **_build_PDF_**: It will take raw_data and file_name of pdf as input and return filename and pdfUrl.
  4.  **_upload_PDF_**: This will upload pdf to server or to any other storage and return its filename.
  5.  **_retrieve_PDF_**: This will take pdf name as input and return pdf content.

-. If we need to add more function in class which needs to be accessible from pdfbase class then they should be first define in PDFPlugin interface.

### 2.2 Adding the plugin to the main system

- Import PDFBuilder Class `from internal import PDFBuilder, PDFPlugin`
- Import Plugin File `from google_doc_plugin.external import GoogleDocsSheetsPlugin`

- Add this class as plugin of PdfBuilder class and also pass config if we need any

```python
config = {"retries": 1, "max_concurrency": 2}
app = PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=config)
```

### 2.3 Starting the system

Just run the following to test if everything is working fine. `app.run()`

Now `main.py` will look like :

```python
from .internal import PDFBuilder, PDFPlugin
from plugin.google_doc_plugin.external import GoogleDocsSheetsPlugin

if __name__ == "__main__":
    config = {"retries": 1, "max_concurrency": 2}
    app = PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=config)
    app.run()
```

## 3. Extending a Plugin already written

A lot of times you wouldn't want to write the whole thing and would want to just extend some other plugin that is already written or maybe two and modify the parts that are not the same as the origin plugin. Here you can do this native python classes.

- Import the plugin to your plugin folder `from google_doc_plugin.external import GoogleDocsSheetsPlugin`
- Create plugin class by extending this superclass and not extending it though the interface. `class ODKPlugin(GoogleDocsSheetsPlugin)`
- All the superclass method are available here. If we need to override the superclass method then we can simply add the method with same name and argument and we can also call the superclass method using super statement. for example : File [google_doc_plugin/external.py](https://github.com/ChakshuGautam/PDF-Package/blob/master/src/plugin/google_doc_plugin/external.py)

```python
from pdfbase.internal import PDFPlugin
from interface import implements

class GoogleDocsSheetsPlugin(implements(PDFPlugin)):
    def __init__(self):
      with open(os.path.dirname(__file__) + '/googledoc-config.json') as json_file:
          config = json.load(json_file)
          self.config = config

    def fetch_data(self):
      return mappingValues,tags, error
```

File [odk_plugin/external.py](https://github.com/ChakshuGautam/PDF-Package/blob/master/src/plugin/odk_plugin/external.py)

```python
from google_doc_plugin.external import GoogleDocsSheetsPlugin

class ODFPlugin(GoogleDocsSheetsPlugin):
    def fetch_data(self):
          return mappingValues,tags, error
    def get_mapping_data(self):
        super().fetch_data()`
```

## 3. FAQs

To be added based on incoming feedback

## 4. Coming Soon

Please review the following section to get information about planned updates to this module.
