"""
Plugin for getting data from another server and generate pdf from it
"""
import json
import os.path
import gspread
import traceback

from oauth2client.service_account import ServiceAccountCredentials
from flask import request
from kafka import KafkaProducer
from utils.func import initialize_logger
from pdfbase.config import KAFKA_CREDENTIAL
from ..google_doc_plugin.external import GoogleDocsSheetsPlugin

# implement interface

class ODKSheetsPlugin(GoogleDocsSheetsPlugin):
    """
    Plugin class which extend from GoogleDocPlugin
    """
    def __init__(self):
        """
        get googledoc-config.json file content and then save this dtaa to class config variable
        """
        logging = initialize_logger()
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)

        with open(os.path.dirname(__file__) + '/config.json') as json_file:
            config = json.load(json_file)
            self.config = config
        self.raw_data = None
        self.tags = None

    def get_tags(self):
        """
        this method return all the tags on the basis of which we filter the request
        """
        tags = dict()
        if self.raw_data:
            tags["FORMID"] = self.raw_data["FORMID"]
            tags["USERNAME"] = self.raw_data["USERNAME"]
            tags["FORMSUBMISSIONDATE"] = self.raw_data["FORMSUBMISSIONDATE"]
            tags["INSTANCEID"] = self.raw_data["INSTANCEID"]
            tags["FORMNAME"] = self.config[self.raw_data["FORMID"]]["FORMNAME"]
            self.config["SHEETID"] = self.config[self.raw_data["FORMID"]]["SHEETID"]
            self.config["DOCTEMPLATEID"] = self.config[self.raw_data["FORMID"]]["DOCTEMPLATEID"]
            self.config["APPLICATIONID"] = self.config[self.raw_data["FORMID"]]["APPLICATIONID"]
            self.config['FORMNAME'] = tags["FORMNAME"]
            if 'FILENAMEFIELD' in self.config[self.raw_data["FORMID"]]:
                self.config['FILENAMEFIELD'] = self.config[self.raw_data["FORMID"]]["FILENAMEFIELD"]
        self.tags = tags
        return tags

    def _get_token(self):
        """ The file token.pickle stores the user's access and refresh tokens, and is
         created automatically when the authorization flow completes for the first
         time."""
        client = None
        try:
            sheet_scopes = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
                ]
            base_path = os.path.dirname(__file__)
            creds_file_path = self.config[self.tags['FORMID']]['GOOGLE_APPLICATION_CREDENTIALS']
            creds = ServiceAccountCredentials.from_json_keyfile_name(base_path+'/'+creds_file_path,
                                                                     sheet_scopes)
            client = gspread.authorize(creds)
        except Exception as ex:
            print(ex)
            self.logger.error("Exception occurred", exc_info=True)
        return client, creds


    def fetch_data(self):
        """
        this method fetches the data from google sheet and return it as raw_data and also send tag
        """
        error = None
        tags = None
        try:
            # Converting unicodes to str and then str to dict.
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
            else:
                raw_data['is_delete'] = True
            kafka_producer = self.connect_kafka_producer()
            value = json.dumps(raw_data)
            error = self.publish_message(kafka_producer, KAFKA_CREDENTIAL['topic'],
                                         KAFKA_CREDENTIAL['group'], value)
            print(json.dumps(self.raw_data, indent=4))
            self.logger.info("Step0 End - instance id %s - Form id %s", instance_id, form_id)
        except Exception as ex:
            print(traceback.format_exc())
            error = "Failed to fetch mapping detials"
            self.logger.error("Error0 %s", error)
            self.logger.error("Exception occurred", exc_info=True)
        return error
    
    
