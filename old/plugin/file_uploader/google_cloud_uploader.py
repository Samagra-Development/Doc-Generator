"""
Class for using google cloud as a storage
"""
from datetime import datetime
from datetime import timedelta
from google.cloud import storage
from utils.func import initialize_logger


class GoogleCloudUploader:
    """
    Class for using google cloud as a storage
    """
    def __init__(self, config_file):
        """
        get googledoc-config.json file content and then initialize storage client
        """
        logging = initialize_logger()
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        self.storage_client = storage.Client.from_service_account_json(config_file)

    def upload_file(self, file_name, bucket_name, key_name):
        """
        bucket: name of bucket
        file_name: local file which we save on google cloud
        key_name: name of file on google cloud
        """
        error = None
        status = None
        expires_in = None
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.blob(key_name)  # giving input the full file name
            blob.upload_from_filename(file_name)
            url_array = self.get_object_url(bucket_name, key_name)
            object_url = url_array[0]
            expires_in = url_array[1]
            if not object_url:
                error = "Failed to get file url"
            else:
                status = object_url
        except Exception as ex:
            error = 'File not uploaded'
            self.logger.error("Exception occurred", exc_info=True)
        return status, error, expires_in
    def get_object_url(self, bucket_name, key_name):
        """Generate a presigned URL to share an google cloud object

        :param bucket_name: string
        :param key_name: string
        :return: Presigned URL,Expiration timestamp as string. If error, returns None.
        """
        doc_url = None
        expires_timestamp = None
        try:
            bucket = self.storage_client.get_bucket(bucket_name)
            blob = bucket.get_blob(key_name)
            year_days = 80*365
            expires_in = timedelta(days=year_days)
            later_date = datetime.now() + timedelta(days=year_days)
            expires_timestamp = datetime.timestamp(later_date)
            doc_url = blob.generate_signed_url(expires_in)

        except Exception as ex:
            self.logger.error("Exception occurred", exc_info=True)

        return doc_url, expires_timestamp
