from interface import Interface


class Uploader(Interface):
    """
    Interface for Uploader
    """

    def put(self, file_name, bucket, object_name):
        """
        Upload file to Location
            bucket: name of bucket
            file_name: local file which we save on google cloud
            key_name: name of file on google cloud
        """
        pass

    def get_object(self, bucket_name, object_name):
        """
        Get file from Location
            bucket: name of bucket
            file_name: local file which we save on google cloud
            key_name: name of file on google cloud
        """
        pass

    def get_signed_url(self, bucket_name, object_name):
        """
        Generate a presigned URL to share an S3 object
            :param bucket_name: string
            :param object_name: string
            ::return: Presigned URL,Expiration timestamp as string. If error, returns None.
        """
        pass
