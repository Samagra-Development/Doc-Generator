from .internal import PDFBuilder, PDFPlugin
from plugin.GoogleDocPlugin.external import GoogleDocsSheetsPlugin
from plugin.ODKPlugin.external import ODKSheetsPlugin

if __name__ == "__main__":
    config = {"retries": 3, "max_concurrency": 2}
    app = PDFBuilder(plugin=GoogleDocsSheetsPlugin(), config=config)
    app.start()