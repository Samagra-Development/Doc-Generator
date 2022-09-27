import json
import os
import traceback
from datetime import datetime, timedelta

import requests
import xmltodict
from django.http import JsonResponse
from interface import implements
import logging

from minio import Minio
from requests import HTTPError

from ..base.interfaces.uploader import Uploader


class GenericMinioUploader(implements(Uploader)):

    def __init__(self, host, username, password, bucket_name):
        self.host = host
        self.bucket_name = bucket_name
        # Get the logger specified in the file
        self.logger = logging.getLogger()
        # Create a client with the MinIO, its access key and secret key.
        self.client = Minio(host, access_key=username, secret_key=password, secure=False)

    def put(self, file_name, object_name, expires):
        error_code = error_msg = None
        final_data = dict()
        try:
            found = self.client.bucket_exists(self.bucket_name)
            if not found:
                self.client.make_bucket(self.bucket_name)

            file_loc = f'pdf/drivefiles/{file_name}'
            result = self.client.fput_object(
                self.bucket_name, object_name, file_loc,
            )
            self.logger.info(
                "created {0} object; etag: {1}, version-id: {2}".format(
                    result.object_name, result.etag, result.version_id,
                ),
            )
            # get signed url
            error_code, error_msg, url = self.get_signed_url(file_name, expires)
            final_data['url'] = url
            final_data['meta'] = {
                "bucket_name": self.bucket_name,
                "object_name": result.object_name,
                "etag": result.etag,
                "version_id": result.version_id,
            }
        except Exception as e:
            traceback.print_exc()
            error_code = 807
            error_msg = f"Failed to upload the file: {e}"
        finally:
            return error_code, error_msg, final_data

    def get_signed_url(self, object_name, expires):
        error_code = error_msg = final_data = None
        try:
            if expires is None:
                final_data = self.get_public_url(object_name)
            else:
                final_data = self.client.presigned_get_object(self.bucket_name, object_name,
                                                              expires=expires)  # expires=timedelta(hours=2)
            self.logger.info(f"url: {final_data}")
        except Exception as e:
            traceback.print_exc()
            error_code = 808
            error_msg = f"Failed to fetch the file: {e}"
        finally:
            return error_code, error_msg, final_data

    def get_object(self, object_name):
        """
        Get file from Location
            bucket: name of bucket
            file_name: local file which we save on google cloud
            key_name: name of file on google cloud
        """
        pass

    def get_public_url(self, file_name):
        return f"http://{self.host}/{self.bucket_name}/{file_name}"
