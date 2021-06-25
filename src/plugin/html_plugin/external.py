"""
Plugin for getting data from sheet and generate pdf from it
"""
import json
import os
import os.path
import calendar
import time
from datetime import datetime
from urllib.parse import urlencode
import traceback
import gspread
from gspread.exceptions import SpreadsheetNotFound
import requests
from requests.auth import HTTPDigestAuth
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from interface import implements
from kafka import KafkaProducer
from confluent_kafka import Consumer, Producer
from ..odk_plugin.external import ODKSheetsPlugin
from pdfbase.config import KAFKA_CREDENTIAL
from plugin.file_uploader.file_uploader import FileUploader
from utils.func import initialize_logger, send_whatsapp_msg, info_log, send_mail
import traceback



def delivery_report(err, msg):
    """ Called once for each message produced to indicate delivery result.
        Triggered by poll() or flush(). """
    if err is not None:
        print('Message delivery failed: {}'.format(err))
    else:
        print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))


# implement interface
class HTMLPlugin(ODKSheetsPlugin):
    """
    Converts HTML to PDF
    """
    def __init__(self):
        """
        get googledoc-config.json file content and then save this dtaa to class config variable
        """
        logging = initialize_logger()
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        print(os.path.dirname(__file__))
        with open(os.path.dirname(__file__) + '/config.json') as json_file:
            config = json.load(json_file)
            self.config = config
        print(self.config)
        self.raw_data = None
        self.tags = None


    def _get_token(self):
        """ The file token.pickle stores the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time."""
        client = None
        creds = None
        try:
            sheet_scopes = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            base_path = os.path.dirname(__file__)
            print("Base path: ", base_path)
            creds = ServiceAccountCredentials.from_json_keyfile_name(base_path + '/gcs-creds.json',
                                                                     sheet_scopes)
            client = gspread.authorize(creds)
        except Exception as ex:
            print(ex)
            self.logger.error("Exception occurred", exc_info=True)
        return client, creds


    def _get_session_cookie(self):
        error = cookie = None
        cookie_request = requests.get(
            self.raw_data['SESSIONCOOKIEBASEURL'],
            auth=HTTPDigestAuth(self.raw_data['ODKUSERNAME'],
                                self.raw_data['ODKPASSWORD']),
            timeout=10)  # Sending the digest authorization request
        headers = str(cookie_request.headers)

        if cookie_request.status_code == 200:  # Check if request is OK
            start_index = headers.find('JSESSIONID=')
            end_index = headers.find(';')
            session_cookie = headers[
                start_index + 11:
                end_index]  # Getting the value of json cookie from the string
            if len(session_cookie) == 32:  # Making sure got the cookie value right
                cookie = session_cookie  # Saving the cookie value
            else:
                error = "No session cookie found"
        else:
            error = "Authorization error"

        return error, cookie


    def build_pdf(self, raw_data, file_name):
        """
        this method get raw_data and file name and generate pdf having this file_name
        """
        print("HELLO! About to try building a PDF")
        error = None
        pdf_name = ''
        pdf_url = ''
        try:
            data = raw_data['req_data']
            info_log(self.logger.info, "Step4 Build Pdf Start", self.raw_data)
            mapping_values = raw_data['value_mapping']
            options_mapping = raw_data['options_mapping']
            mapped_data = self.map_data(data, mapping_values, options_mapping)
            mapping_error = mapped_data[1]
            final_data = mapped_data[0]
            print(final_data)
            # if not mapping_error:
            #     # URL of google app script
            #     final_data_str = json.dumps(final_data)
            #     if 'FILENAMEFIELD' in raw_data and raw_data['FILENAMEFIELD'] in data:
            #         file_name = data[raw_data['FILENAMEFIELD']] + '_' + str(
            #             calendar.timegm(time.gmtime()))
            #     print(file_name)
            #     payload = {
            #         "fileName": file_name,
            #         "mylist": final_data_str,
            #         "templateId": raw_data['DOCTEMPLATEID']
            #     }  # Encoding the url with payload
            #     if ('ODKUSERNAME' in self.raw_data.keys() and self.raw_data['ODKUSERNAME']
            #             and 'ODKPASSWORD' in self.raw_data.keys() and self.raw_data['ODKPASSWORD']):
            #         call_session_cookie = self._get_session_cookie()

            #         if not call_session_cookie[0]:
            #             session_cookie = call_session_cookie[1]
            #         else:
            #             error = call_session_cookie[0]

            #         if not error:
            #             payload['sessionCookie'] = session_cookie
            #             payload['username'] = self.raw_data['ODKUSERNAME']
            #             payload['password'] = self.raw_data['ODKPASSWORD']
            #     if not error:
            #         gas_url = self.config['URL'] + urlencode(payload)
            #         # Calling the GAS url and Getting the GAS response

            #         app_script_response = self._generate_file_drive(gas_url)
            #         error = app_script_response[3]

            #         if not error:
            #             pdf_url = app_script_response[2]
            #             pdf_name = app_script_response[1] + '.pdf'
            #             print(pdf_url, pdf_name)

            # else:
            #     error = mapping_error
            # info_log(self.logger.info, "Step4 Build Pdf End", self.raw_data)

        except Exception as ex:
            error = "Failed to generate pdf"
            info_log(self.logger.error, "Error2 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
            print(traceback.format_exc())
        return pdf_name, error, pdf_url
    

    def fetch_data(self, req_data=""):
        """
        this method fetches the data from google sheet and return it as raw_data and also send tag
        """
        print("FETCHING DATA!!!")
        error = None
        tags = None
        try:
            req_data = json.loads(json.dumps(request.json))
            # Getting the form ID to distinguish between various template document and mapping sheet
            form_id = req_data['formId']
            new_req_data = req_data['data'][0]  # Getting the data : [{values}]
            instance_id = new_req_data['instanceID']  # Getting the instance id for searching routes
            self.logger.info("Step0 Start - instance id %s - Form id %s", instance_id, form_id)
            user_name_field = self.config[form_id]["USERNAMEFIELD"]
            new_req_data = json.loads(json.dumps(new_req_data))  # Getting the new data
            user_name = new_req_data[user_name_field]
            form_submission_date = new_req_data[
                '*meta-submission-date*']  # Correcting the submission date and removing the time
            end_index = form_submission_date.find(str('T'))
            form_submission_date = form_submission_date[:end_index]
            # Saving the corrected date in the json
            new_req_data['*meta-submission-date*'] = form_submission_date
            my_dict = {}
            for req_key, req_val in new_req_data.items():
                if isinstance(req_val, dict):
                    for col_key, col_val in req_val.items():
                        if col_key == "url":
                            # correcting the URLs
                            base_url = 'http://aggregate.cttsamagra.xyz:8080/'
                            index_start = 0  # Finding the substring
                            index_end = col_val.find(
                                ":8080/") + 6  # Find the stopping point
                            newv1 = col_val.replace(col_val[index_start:index_end], base_url)
                            my_dict[req_key] = newv1
                elif isinstance(req_val, (float, int)):
                    my_dict[req_key] = str(req_val)
                elif isinstance(req_val, list):
                    my_dict[req_key] = str(req_val[0])  # Converting list to str
                else:
                    if req_val is None:
                        req_val = "-"
                    my_dict[req_key] = req_val

            # Calculate Udise from its database and then Calculate distance from udise
            calculated_distance = 'Not available'  # Calculate using udise
            my_dict['calculated_distance'] = calculated_distance
            all_data = dict()
            all_data['req_data'] = my_dict
            all_data['FORMID'] = form_id
            all_data['INSTANCEID'] = instance_id
            all_data['USERNAME'] = user_name
            all_data['FORMSUBMISSIONDATE'] = form_submission_date
            self.raw_data = all_data
            tags = self.get_tags()
            all_data.update(self.config)
            raw_data = dict()
            raw_data['reqd_data'] = all_data
            raw_data['tags'] = tags
            raw_data['instance_id'] = instance_id
            if 'DOCDELETED' in self.config[self.raw_data["FORMID"]]:
                raw_data['is_delete'] = self.config[self.raw_data["FORMID"]]["DOCDELETED"]
            # kafka_producer = self.connect_kafka_producer()
            # value = json.dumps(raw_data)
            # error = self.publish_message(kafka_producer, KAFKA_CREDENTIAL['topic'],
            #                              KAFKA_CREDENTIAL['group'], value)
            else:
                raw_data['is_delete'] = True
            print(self.raw_data)
            self.logger.info("Step0 End - instance id %s - Form id %s", instance_id, form_id)
            return raw_data, None
        except Exception as ex:
            print(traceback.format_exc())
            error = "Failed to fetch mapping detials"
            self.logger.error("Error0 %s", error)
            self.logger.error("Exception occurred", exc_info=True)
        return None, "Failed to complete fetching data"
    
    def publish_message(raw_data=""):
        kafka_producer = self.connect_kafka_producer()
        value = json.dumps(raw_data)
        error = self.publish_message(kafka_producer, KAFKA_CREDENTIAL['topic'],
                                         KAFKA_CREDENTIAL['group'], value)