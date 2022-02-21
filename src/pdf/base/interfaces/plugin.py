from celery import shared_task
from interface import Interface


class Plugin(Interface):
    """
    **FetchData.process() -> Dict  => Fetches "new" data from the database/server/websocket
    whatever and provides it in the form of dictionary, one PDF at a time.
    **FetchTemplate.process() -> Dict => Fetches mapping and yields it in the form of dictionary
    **BuildPDF.process() -> File => Function to build PDF and return a file
    **UploadPDF.process(key, File) ->  => Function to save PDF
    **RetrievePDF.process(key) -> File => Function to get the previously saved PDF from the key
    **Publish.process(key) -> File => Function to send the response to external url/webhook
    """

    def fetch_data(self):
        """
        Fetches "new" data from the database/server/websocket
        whatever and provides it in the form of dictionary, one PDF at a time
        """

    def fetch_template(self, template_id):
        """
        Fetches template and returns it in the form of string
        """

    def build_file(self, template_id, token):
        """
        Function to build PDF and return a file (fetch template and build pdf)
        """

    def upload_file(self, template_id, token):
        """
        Function to save PDF
        """

    def retrieve_file(self, key):
        """
        Function to get the previously saved PDF from the key
        """

    def shorten_url(self, template_id, hash_id):
        """
        Function to generate short url for the uploaded doc
        """
        pass

    def publish(self, id, url, headers):
        """
        Function to publish response on external url/webhook
        """
        pass
