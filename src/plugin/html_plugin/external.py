"""
Plugin for getting data from another server and generate pdf from it
"""
import json
import os.path
import gspread
import traceback
import html

from oauth2client.service_account import ServiceAccountCredentials
from flask import request
from kafka import KafkaProducer
import requests
from utils.func import initialize_logger
from pdfbase.config import KAFKA_CREDENTIAL
from plugin.file_uploader.file_uploader import FileUploader
from utils.func import initialize_logger, info_log
import calendar
import time
import pdfkit
from ..google_doc_plugin.external import GoogleDocsSheetsPlugin

# implement interface

class HTMLPlugin(GoogleDocsSheetsPlugin):
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
        return tags


    def fetch_data(self):
        """
        Fetches template, configuration, mapping and updates the request JSON to
        include these values directly
        """
        error = None
        tags = None
        try:
            req_data = json.loads(json.dumps(request.json))
            form_id = req_data['formId']
            new_req_data = req_data['data'][0]  # Getting the data : [{values}]
            instance_id = new_req_data['instanceID']  # Getting the instance id for searching routes
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
            all_data["SHEETID"] = self.config[form_id]["SHEETID"]
            
            all_data["DOCTEMPLATEID"] = self.config[form_id]["DOCTEMPLATEID"]
            all_data["APPLICATIONID"] = self.config[form_id]["APPLICATIONID"]
            self.raw_data = all_data

            # Update the config with config from the currently used template
            tags = self.get_tags()
            all_data.update(self.config)

            raw_data = dict()
            raw_data['reqd_data'] = all_data
            raw_data['tags'] = tags
            raw_data['instance_id'] = instance_id
            
            if 'DOCDELETED' in self.config[all_data["FORMID"]]:
                raw_data['is_delete'] = self.config[all_data["FORMID"]]["DOCDELETED"]
            else:
                raw_data['is_delete'] = True

            # Push the information to queue so that PDF generation can start
            kafka_producer = self.connect_kafka_producer()
            value = json.dumps(raw_data)
            error = self.publish_message(kafka_producer, KAFKA_CREDENTIAL['topic'],
                                         KAFKA_CREDENTIAL['group'], value)
            self.logger.info("Step0 End - instance id %s - Form id %s", instance_id, form_id)
        except Exception as ex:
            print(traceback.format_exc())
            error = "Failed to fetch mapping detials"
            self.logger.error("Error0 %s", error)
            self.logger.error("Exception occurred", exc_info=True)
        return error

    
    def build_pdf(self, raw_data, file_name):
        """
        Fills in template values and generates the PDF
        The PDF file is stored locally and the file name is returned for further 
        processing/uploading
        """
        error = None
        pdf_name = None
        pdf_url = None
        pdf_path = None
        try:
            print("Starting process")
            data = raw_data['req_data']
            mapping_values = raw_data['value_mapping']
            options_mapping = raw_data['options_mapping']

            # Get data mapping for the template

            mapped_data = self.map_data(data, mapping_values, options_mapping)
            print("Mapped Data Obtained")
            html_content = requests.get("https://docs.google.com/document/d/" + self.config["DOCTEMPLATEID"] + "/export?format=html").content
            html_content = html.unescape(html_content.decode('utf-8'))
            
            # Check if filename is specified in the config and if so, use that instead 
            # rather than the value passed to the method
            if 'FILENAMEFIELD' in raw_data and raw_data['FILENAMEFIELD'] in data:
                file_name = data[raw_data['FILENAMEFIELD']] + '_' + str(
                    calendar.timegm(time.gmtime()))

            # Fill in template values
            # TODO: Image template values
            # TODO: Iterate other way (find the values to fill in from HTML and fill those in
            # so that error checking will be possible)
            for idx, val in enumerate(mapped_data[0]):
                template_index = idx + 1
                string_to_search = '<<' + str(template_index) + '>>'
                html_content = html_content.replace(string_to_search, val)

            # Check if the folder to write to exists, and if not make it.
            base_path = os.path.join(os.path.abspath(''), self.config['DIRPATH'])
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            
            # Write HTML file with filled template values
            file_path = os.path.join(base_path, 'filled_template.html')
            with(open( file_path, 'w') as f):
                f.write(html_content)
            
            # Convert filled HTML file to PDF
            # TODO: pdfkit here requires wkhtmltopdf installed on the PDF
            # Consider alternatives that don't have this requirement
            # xhmtl2pdf, weasyprint, pyppeteer (Chromium based)
            with open(file_path) as f:
                pdf_name = file_name
                file_name = file_name + ".pdf"    
                pdf_path = os.path.join(base_path, file_name)
                pdfkit.from_file(f, pdf_path)
        except Exception as ex:
            error = "Failed to generate pdf"
            info_log(self.logger.error, "Error2 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        print("PDF Builder Complete")
        return pdf_name, error, pdf_url, pdf_path
    

    def _upload_file(self, base_path, file_path, key):
        """
        Uploads the generated PDF at `file_path` to either S3 or Google Cloud
        based on the configuration
        """
        if ('UPLOADTO' in self.config.keys() and self.config['UPLOADTO']):
            if self.config['UPLOADTO'] == 's3':
                cdn_upload = FileUploader(self.config['UPLOADTO'], self.config['ACCESSKEY'],
                                            self.config['SECRETKEY'])
            else:
                base_path = os.path.dirname(__file__)
                print(self.config['UPLOADTO'],
                                            base_path + '/' + 
                                            self.config['GOOGLE_APPLICATION_CREDENTIALS'])
                cdn_upload = FileUploader(self.config['UPLOADTO'],
                                            base_path + '/' +
                                            self.config['GOOGLE_APPLICATION_CREDENTIALS'])
            resp = cdn_upload.upload_file(file_path,
                                            self.config['BUCKET'], key)
            url = resp[0]
            error = resp[1]
            if url:
                upload_file_url = url
                expire_timestamp = resp[2]
                os.remove(file_path)
            else:
                print("Error6 " + error, self.raw_data)

            print("Step5.1 Upload To Cdn End", self.raw_data)
            return upload_file_url, error, expire_timestamp


    def upload_pdf(self, key, file_url, file_path=None):
        """
        Uploads to Google Cloud or AWS
        TODO: Uploading to local server
        """
        print("UPLOADING PDF!")
        print(file_url, file_path, key)
        error = ''
        upload_file_url = None
        expire_timestamp = None
        try:
            if not file_url and not file_path:
                error = "Please specify either file URL or file path"
                return "", error, ""
            if file_path:
                base_path = os.path.join(os.path.abspath(''))            
                upload_file_url, error, expire_timestamp = self._upload_file(base_path, file_path, key)
                print(print, "Step5 Upload Pdf End", self.raw_data)

        except Exception as ex:
            error = "Failed to download file from drive"
            print("Error5 " + error, self.raw_data)
            print("Exception occurred")
            print(traceback.format_exc())
        return upload_file_url, error, expire_timestamp