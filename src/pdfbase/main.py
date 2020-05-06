"""
Initializes pdf builder and start the server
"""
from .internal import PDFBuilder
from plugin.google_doc_plugin.external import GoogleDocsSheetsPlugin
from plugin.odk_plugin.external import ODKSheetsPlugin

if __name__ == "__main__":
    CONFIG = {"retries": 20, "max_concurrency": 1}
    APP = PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=CONFIG)
    APP.start()
