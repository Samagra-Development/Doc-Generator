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


def get_fa_token(username, password):
    token = None
    try:
        body = json.dumps({
            "loginId": f"{username}",
            "password": f"{password}",
            "applicationId": "2011a6c9-7fb7-4306-8c6d-c96cb07c7859"
        })
        headers = {
            'Content-Type': 'application/json',
            'Authorization': 'YFpyHxhW0-NoKRwQrXgCU5QIAQq8nBNhE--i5_n3pTU'
        }
        response = requests.post("http://auth.samagra.io:9011/api/login", data=body, headers=headers)
        response.raise_for_status()
        resp = response.json()
        if 'token' in resp:
            token = resp['token']
        else:
            raise Exception("short url not generated")
    except Exception as e:
        traceback.print_exc()
        print(f"Something went wrong: {e}")
    finally:
        return token


def get_minio_cred(username, password, bucket_name):
    access_key = secret_key = session_token = None
    try:
        token = get_fa_token(username, password)
        if token is not None:
            minio_url = f"https://cdn.samagra.io/minio/{bucket_name}/?Action=AssumeRoleWithWebIdentity&DurationSeconds=36000&WebIdentityToken={token}&Version=2011-06-15"
            response = requests.post(minio_url)
            response.raise_for_status()
            resp = response.text
            xml_data = xmltodict.parse(resp)
            access_key = \
            xml_data['AssumeRoleWithWebIdentityResponse']['AssumeRoleWithWebIdentityResult']['Credentials'][
                'AccessKeyId']
            secret_key = \
            xml_data['AssumeRoleWithWebIdentityResponse']['AssumeRoleWithWebIdentityResult']['Credentials'][
                'SecretAccessKey']
            session_token = \
            xml_data['AssumeRoleWithWebIdentityResponse']['AssumeRoleWithWebIdentityResult']['Credentials'][
                'SessionToken']
        else:
            raise Exception("Failed to fetch FA token")
    except Exception as e:
        traceback.print_exc()
        print(f"Something went wrong: {e}")
    finally:
        return access_key, secret_key, session_token


class MinioUploader(implements(Uploader)):

    def __init__(self, host, username, password, bucket_name):
        self.host = host
        self.bucket_name = bucket_name
        # Get the logger specified in the file
        self.logger = logging.getLogger()
        # Create a client with the MinIO, its access key and secret key.
        access_key, secret_key, session_token = get_minio_cred(username, password, bucket_name)
        self.client = Minio(host, access_key=access_key, secret_key=secret_key, session_token=session_token)

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
        return f"https://{self.host}/{self.bucket_name}/{file_name}"
