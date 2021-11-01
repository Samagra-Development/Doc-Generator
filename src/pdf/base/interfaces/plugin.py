from interface import Interface


class Plugin(Interface):
    """
    **FetchData.process() -> Dict  => Fetches "new" data from the database/server/websocket
    whatever and provides it in the form of dictionary, one PDF at a time.
    **FetchMapping.process() -> Dict => Feches mapping and yeilds it in the form of dictionary
    **BuildPDF.process() -> File => Function to build PDF and return a file
    **UploadPDF.process(key, File) ->  => Fuction to save PDF
    **RetrievePDF.process(key) -> File => Function to get the previously saved PDF from the key
    """

    def fetch_data(self):
        """
        Fetches "new" data from the database/server/websocket
        whatever and provides it in the form of dictionary, one PDF at a time
        """

    def fetch_mapping(self, data):
        """
        Feches mapping and yeilds it in the form of dictionary
        """

    def build_pdf(self, raw_data, file_name):
        """
        Function to build PDF and return a file
        """

    def upload_pdf(self, key, file_url):
        """
        Fuction to save PDF
        """

    def retrieve_pdf(self, key):
        """
        Function to get the previously saved PDF from the key
        """

    def delete_file_drive_google_script(self, file):
        """
        Function to delete doc from drive
        :param file:
        :return:
        """

    def shorten_url(self, url, doc_url):
        pass

    def set_raw_data(self, raw_data):
        pass
