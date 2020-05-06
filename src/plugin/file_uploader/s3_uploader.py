"""
Class for using s3 as a storage
"""
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
class S3Uploader:
    """
    Class for using s3 as a storage
    """
    def __init__(self, aws_access_key, aws_secret_key):
        """
        Intialize s3 client
        """
        self.s3_client = boto3.resource("s3",
                                        aws_access_key_id=aws_access_key,
                                        aws_secret_access_key=aws_secret_key
                                        )
        self.bucket_resource = self.s3_client
        #self.bucket = bucket
    def upload_file(self, file_name, bucket, object_name):
        """Upload a file to an S3 bucket
        :param file_name: File to upload
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        :return: True if file was uploaded, else False
        """
        error = None
        status = True

        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        try:
            print('in s3 upload')
            response = self.s3_client.meta.client.upload_file(file_name, bucket, object_name)
            print('after s3 upload')
            print(response)
        except S3UploadFailedError as ex:
            print(ex)
            print('in s3 error')
            error = "Failed to Upload Files"
            status = False
        except ClientError as ex:
            print(ex)
            print('in s3 error')
            error = "Failed to Upload Files"
            status = False
        except Exception as ex:
            error = "Failed to Upload Files"
            status = False
        return status, error
