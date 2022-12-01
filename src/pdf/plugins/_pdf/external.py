import json
import os
import traceback

from celery import shared_task
from interface import implements
import pdfkit
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

from ...base.interfaces.plugin import Plugin
from ...models import GenericConfig
from ...shorteners.yaus import YausShortner
from ...uploaders.minio import MinioUploader
from ...uploaders.generic_minio import GenericMinioUploader
from ...utils import publish_to_url, build_pdf
import requests
from dotenv import load_dotenv

load_dotenv("../../.env")


class PDFPlugin(implements(Plugin)):

    def __init__(self, data, token):
        """
        To do authentication
        """
        # generate path
        try:
            self.config = GenericConfig.objects.get(pk=data['config_id'])
        except KeyError:
            self.config = GenericConfig.objects.get(pk=1)
        self.user_config = json.loads(self.config.data)
        self._data = data['data']
        self.template_id = data['template_id']
        self.token = token
        self.settings_file_loc = f"pdf/creds/{self.user_config['APPLICATION_SETTINGS_FILE']}"
        self.creds_file_location = f"pdf/creds/{self.user_config['CREDENTIAL_SETTINGS_FILE']}"
        self.uploader = self.config.uploader_ref
        self.shortener = self.config.shortener_ref

    def get_client(self):
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

    def fetch_template(self):
        """
        Fetches template and returns it in the form of string
        """
        try:
            template_string = error_code = error_msg = None
            data = json.dumps({
                "id": self.template_id,
                "data": self._data
            })
            headers = {
                'Content-Type': 'application/json'
            }
            response = requests.post(
                f"{os.getenv('TEMPLATOR_URL')}/process", data=data, headers=headers)
            if response.status_code == 201:
                template_string = response.json(
                )['processed'] if "processed" in response.json() else None
            else:
                error = response.text
        except Exception as e:
            traceback.print_exc()
            error_msg = f"Failed to fetch template: {e}"
            error_code = 801
        return error_code, error_msg, template_string

    def build_file(self, template):
        """
        Function to build PDF and return a file (fetch template and build pdf)
        """
        is_successful = error_code = error_msg = None
        drive_file_loc = f'pdf/drivefiles/{self.token}.pdf'
        options = {
            'page-size': 'A4',
            'orientation': 'Portrait',
            'margin-top': '0',
            'margin-bottom': '0',
            'margin-right': '0',
            'margin-left': '0',
            'encoding': 'UTF-8',
            'disable-smart-shrinking': '',
        }
        try:
            # path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
            # config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
            # pdfkit.from_string(template, drive_file_loc, configuration=config)
            # pdfkit.from_string(template, drive_file_loc)
            path_wkhtmltopdf = os.environ.get('WKHTMLTOPDF', None)
            if path_wkhtmltopdf:
                config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
                pdfkit.from_string(template, drive_file_loc,
                                   configuration=config, options=options)
            else:
                pdfkit.from_string(template, drive_file_loc, options=options)
            is_successful = True
        except Exception as e:
            traceback.print_exc()
            error_msg = f"Failed to generate doc: {e}"
            error_code = 803
        return error_code, error_msg, is_successful

    def upload_file(self):
        """
        Function to save PDF
        """
        error_code = error_msg = final_data = None
        try:
            drive_file_loc = f'pdf/drivefiles/{self.token}.pdf'
            if self.uploader == "minio":
                host = self.user_config["MINIO_HOST"]
                access_key = self.user_config["MINIO_ACCESS_KEY"]
                secret_key = self.user_config["MINIO_SECRET_KEY"]
                bucket_name = self.user_config["MINIO_BUCKET_NAME"]
                uploader = MinioUploader(
                    host, access_key, secret_key, bucket_name)
                error_code, error_msg, final_data = uploader.put(
                    f'{self.token}.pdf', f'{self.token}.pdf', None)
                if error_code is None:
                    if os.path.exists(drive_file_loc):
                        os.remove(drive_file_loc)
                else:
                    raise Exception("Failed to build the pdf")
                return error_code, error_msg, final_data
            elif self.uploader == "generic_minio":
                host = self.user_config["MINIO_HOST"]
                access_key = self.user_config["MINIO_ACCESS_KEY"]
                secret_key = self.user_config["MINIO_SECRET_KEY"]
                bucket_name = self.user_config["MINIO_BUCKET_NAME"]
                uploader = GenericMinioUploader(
                    host, access_key, secret_key, bucket_name)
                error_code, error_msg, final_data = uploader.put(
                    f'{self.token}.pdf', f'{self.token}.pdf', None)
                if error_code is None:
                    if os.path.exists(drive_file_loc):
                        os.remove(drive_file_loc)
                else:
                    raise Exception("Failed to build the pdf")
                return error_code, error_msg, final_data
            else:
                raise Exception("Uploader plugin not supported")
        except Exception as e:
            traceback.print_exc()
            error_code = 805
            error_msg = f"Something went wrong: {e}"
        finally:
            return error_code, error_msg, final_data

    def retrieve_file(self, object_name):
        """
        Function to get the previously saved PDF from the key
        """

    def shorten_url(self, url):
        """
        Function to generate short url for the uploaded doc
        """
        error_code = error_msg = final_data = None
        try:
            if self.shortener == "yaus":
                host = self.user_config["SHORTENER_URL"]
                shortener = YausShortner(host)
                error_code, error_msg, final_data = shortener.apply(
                    url, self.token)
                if error_code is None:
                    final_data = final_data['url']
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
