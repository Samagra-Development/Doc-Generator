from interface import Interface


class Uploader(Interface):
    """
    Interface for Uploader
    """

    def put(self, file_name, object_name, expires):
        """
        Upload file to Location
            bucket: name of bucket
            file_name: local file which we save on google cloud
            key_name: name of file on google cloud
        """
        pass

    def get_object(self, object_name):
        """
        Get file from Location
            bucket: name of bucket
            file_name: local file which we save on google cloud
            key_name: name of file on google cloud
        """
        pass

    def get_signed_url(self, object_name, expires):
        """
        Generate a presigned URL to share an S3 object
            :param bucket_name: string
            :param object_name: string
            ::return: Presigned URL,Expiration timestamp as string. If error, returns None.
        """
        pass
