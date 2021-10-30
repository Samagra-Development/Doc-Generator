"""
General module in which depending on the storage use we intialize that class
"""
from .s3_uploader import S3Uploader
from .google_cloud_uploader import GoogleCloudUploader


class FileUploader:

    """
    Super class for storage
    """
    def __init__(self, client, access_key, secret_key=''):
        """
        intialize googlecloud and s3 uploader depending on the storage we use
        """
        if client == 's3':
            self.storage_client = S3Uploader(access_key, secret_key)
        else:
            self.storage_client = GoogleCloudUploader(access_key)
        #self.bucket = bucket

    def upload_file(self, file_name, bucket, object_name):
        """
        calls class respective upload_file method
        """
        return self.storage_client.upload_file(file_name, bucket, object_name)

    def get_object_url(self, bucket_name, object_name):
        """
        call class respective get_object url
        :param bucket_name:
        :param object_name:
        :return:
        """
        return self.storage_client.get_object_url(bucket_name, object_name)
