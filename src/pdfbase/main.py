"""
Initializes pdf builder and start the server
"""
from plugin.html_plugin.external import HTMLPlugin
from .internal import PDFBuilder
#from plugin.odk_plugin.external import ODKSheetsPlugin

if __name__ == "__main__":
    CONFIG = {"retries": 20, "max_concurrency": 1}
    APP = PDFBuilder(plugin=HTMLPlugin(), config=CONFIG)
    APP.start()
