"""
Class for using s3 as a storage
"""
from datetime import datetime
from datetime import timedelta
import boto3
from botocore.exceptions import ClientError
from boto3.exceptions import S3UploadFailedError
from utils.func import initialize_logger


class S3Uploader:
    """
    Class for using s3 as a storage
    """
    def __init__(self, aws_access_key, aws_secret_key):
        """
        Intialize s3 client
        """
        logging = initialize_logger()
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
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
        expires_in = None
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = file_name

        try:
            response = self.s3_client.meta.client.upload_file(file_name, bucket, object_name)

            url_array = self.get_object_url(bucket, object_name)
            object_url = url_array[0]
            expires_in = url_array[1]
            if not object_url:
                error = "Failed to get file url"
            else:
                status = object_url

        except S3UploadFailedError as ex:
            error = "Failed to Upload Files"
            status = False
            self.logger.error("Exception occurred", exc_info=True)
        except ClientError as ex:
            error = "Failed to Upload Files"
            status = False
            self.logger.error("Exception occurred", exc_info=True)
        except Exception as ex:
            error = "Failed to Upload Files"
            status = False
            self.logger.error("Exception occurred", exc_info=True)
        return status, error, expires_in
    def get_object_url(self, bucket_name, object_name):
        """Generate a presigned URL to share an S3 object

        :param bucket_name: string
        :param object_name: string
        ::return: Presigned URL,Expiration timestamp as string. If error, returns None.
        """

        # Generate a presigned URL for the S3 object
        expires_timestamp = None
        response = None
        try:
            #expires_in = 1*365*24*60*60
            year_days = 10*365
            expires_in = year_days*24*60*60
            later_date = datetime.now() + timedelta(days=year_days)
            expires_timestamp = datetime.timestamp(later_date)
            response = self.s3_client.meta.client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name,
                        'Key': object_name},
                ExpiresIn=expires_in,
                HttpMethod="GET")

        except ClientError as ex:
            self.logger.error("Exception occurred", exc_info=True)
            return None

        # The response contains the presigned URL
        return response, expires_timestamp
