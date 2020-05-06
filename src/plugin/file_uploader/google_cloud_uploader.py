"""
Class for using google cloud as a storage
"""
from google.cloud import storage

class GoogleCloudUploader:
    """
    Class for using google cloud as a storage
    """
    def __init__(self, config_file):
        """
        get googledoc-config.json file content and then initialize storage client
        """
        self.storage_client = storage.Client.from_service_account_json(config_file)

    def upload_file(self, file_name, bucket, key_name):
        """
        bucket: name of bucket
        file_name: local file which we save on google cloud
        key_name: name of file on google cloud
        """
        error = None
        status = True
        try:
            bucket = self.storage_client.get_bucket(bucket)
            blob = bucket.blob(key_name)  # giving input the full file name
            blob.upload_from_filename(file_name)
        except Exception as ex:
            error = 'File not uploaded'
            status = False

        return status, error
