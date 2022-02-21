import json
import os
import traceback

from celery import shared_task
from interface import implements
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from ...base.interfaces.plugin import Plugin
from ...models import GenericConfig
from ...shorteners.yaus import YausShortner
from ...uploaders.minio import MinioUploader
from ...utils import publish_to_url, build_pdf
import requests
from dotenv import load_dotenv

load_dotenv("../../.env")


class PDFPlugin(implements(Plugin)):

    def __init__(self, config_id, raw_data):
        """
        To do authentication
        """
        # generate path
        self.config = GenericConfig.objects.get(pk=config_id)
        self.user_config = json.loads(self.config.data)
        self._data = raw_data
        self.settings_file_loc = f"pdf/creds/{self.user_config['APPLICATION_SETTINGS_FILE']}.yaml"
        self.creds_file_location = f"pdf/creds/{self.user_config['CREDENTIAL_SETTINGS_FILE']}.json"
        self.uploader = self.config.uploader_ref
        self.shortener = self.config.shortener_ref

    def get_token(self):
        gauth = GoogleAuth(settings_file=self.settings_file_loc)
        gauth.LoadCredentialsFile(self.creds_file_location)
        if gauth.credentials is None:
            # Authenticate if they're not there
            gauth.CommandLineAuth()
        elif gauth.access_token_expired:
            # Refresh them if expired
            gauth.Refresh()
        else:
            # Initialize the saved creds
            gauth.Authorize()
        # Save the current credentials to a file
        gauth.SaveCredentialsFile(self.creds_file_location)
        drive = GoogleDrive(gauth)
        self.drive = drive
        return self.drive

    def fetch_data(self):
        """
        Fetches "new" data from the database/server/websocket
        whatever and provides it in the form of dictionary, one PDF at a time
        """
        pass

    def fetch_template(self, template_id):
        """
        Fetches template and returns it in the form of string
        """
        data = json.dumps({
            "id": template_id,
            "data": self._data
        })
        headers = {
            'Content-Type': 'application/json'
        }
        response = requests.post(os.getenv('PROCESS_TEMPLATE_URL'), data=data, headers=headers)
        if response.status_code == 201:
            template_string = response.json()['processed'] if "processed" in response.json() else None
            return template_string
        else:
            return None

    def build_file(self, template_id, token):
        """
        Function to build PDF and return a file (fetch template and build pdf)
        """
        is_successful = False
        template = self.fetch_template(template_id)
        if template is not None:
            is_successful = build_pdf(template, token)
        return is_successful

    def upload_file(self, template_id, token):
        """
        Function to save PDF
        """
        error_code = error_msg = final_data = None
        try:
            is_successful = self.build_file(template_id, token)
            print("isSuccessful", is_successful)
            drive_file_loc = f'pdf/drivefiles/{token}.pdf'
            if is_successful:
                if self.uploader == "minio":
                    host = self.user_config["MINIO_HOST"]
                    access_key = self.user_config["MINIO_ACCESS_KEY"]
                    secret_key = self.user_config["MINIO_SECRET_KEY"]
                    bucket_name = self.user_config["MINIO_BUCKET_NAME"]
                    uploader = MinioUploader(host, access_key, secret_key, bucket_name)
                    error_code, error_msg, final_data = uploader.put(f'{token}.pdf', f'{token}.pdf', None)
                    if error_code is None:
                        if os.path.exists(drive_file_loc):
                            os.remove(drive_file_loc)
                    else:
                        raise Exception("Failed to build the pdf")
                    return error_code, error_msg, final_data
                else:
                    raise Exception("Uploader plugin not supported")
            else:
                raise Exception("Failed to upload the pdf")
        except Exception as e:
            traceback.print_exc()
            error_code = 805
            error_msg = f"Something went wrong: {e}"
        finally:
            return error_code, error_msg, final_data

    def retrieve_file(self, key):
        """
        Function to get the previously saved PDF from the key
        """

    def shorten_url(self, template_id, hash_id):
        """
        Function to generate short url for the uploaded doc
        """
        error_code = error_msg = final_data = None
        try:
            error_code, error_msg, url = self.upload_file(template_id, hash_id)
            print("url", error_code, error_msg, url)
            if error_code is None:
                if self.shortener == "yaus":
                    host = self.user_config["SHORTENER_URL"]
                    shortener = YausShortner(host)
                    error_code, error_msg, final_data = shortener.apply(url, hash_id)
                    if error_code is None:
                        final_data = final_data['shortUrl']
                else:
                    raise Exception("Shortener plugin not available")
        except Exception as e:
            traceback.print_exc()
            error_code = 806
            error_msg = f"Something went wrong: {e}"
        finally:
            return error_code, error_msg, final_data

    def publish(self, id, url, headers):
        """
        Function to publish response on external url/webhook
        """
        publish_to_url(id, url, headers=headers)
