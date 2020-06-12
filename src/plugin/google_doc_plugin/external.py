"""
Plugin for getting data from sheet and generate pdf from it
"""
import json
import os
import os.path
import calendar
import time
from urllib.parse import urlencode
import gspread
from gspread.exceptions import SpreadsheetNotFound
import requests
from requests.auth import HTTPDigestAuth
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from interface import implements
from kafka import KafkaProducer
import pyshorteners
from pdfbase.internal import PDFPlugin
from plugin.file_uploader.file_uploader import FileUploader
from utils.func import initialize_logger, send_whatsapp_msg, info_log, send_mail


# implement interface

class GoogleDocsSheetsPlugin(implements(PDFPlugin)):
    """
    Plugin class which implement PDFPlugin interface
    """

    def __init__(self):
        """
        get googledoc-config.json file content and then save this data to class config variable
        """
        logging = initialize_logger()
        # Get the logger specified in the file
        self.logger = logging.getLogger(__name__)
        with open(os.path.dirname(__file__) + '/googledoc-config.json') as json_file:
            config = json.load(json_file)
            self.config = config
        self.raw_data = None
        self.tags = None

    def set_raw_data(self, raw_data):
        """
        initialize raw data
        :param raw_data:
        :return:
        """
        self.raw_data = raw_data

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

    def get_sheetvalues(self, sheet_id, var_mapping):
        """
        get google sheet data of the specified sheet id and range
        """
        error = None
        try:
            client = self._get_token()[0]
            base_sheet = client.open_by_key(sheet_id)
            sheet = base_sheet.worksheet(var_mapping)
            values = sheet.get_all_values()
            # print(values)
            if not values:
                error = "No Mapping details found"
            else:
                mapping_values = values
        except SpreadsheetNotFound as ex:
            error = "Failed to fetch mapping detials"
            mapping_values = None
            self.logger.error("Exception occurred", exc_info=True)
        except Exception as ex:
            error = "Failed to fetch mapping detials"
            mapping_values = None
            self.logger.error("Exception occurred", exc_info=True)
        return mapping_values, error

    def get_tags(self):
        """
        this method return all the tags on the basis of which we filter the request
        """
        tags = dict()
        tags["SHEETID"] = self.config["SHEETID"]
        tags["SHEETNAME"] = self.config["SHEETNAME"]
        tags["RANGE"] = self.config["RANGE"]
        tags["MAPPINGDETAILS"] = self.config["MAPPINGDETAILS"]
        tags["OPTIONSSHEET"] = self.config["OPTIONSSHEET"]
        tags["DOCTEMPLATEID"] = self.config["DOCTEMPLATEID"]
        tags["APPLICATIONID"] = self.config["APPLICATIONID"]
        self.tags = tags
        return tags

    def publish_message(self, producer_instance, topic_name, key, value):
        """
        publish message to kafka
        :param producer_instance:
        :param topic_name: name of topic
        :param key: message key
        :param value: message value
        :return: status
        """
        error = ''
        try:
            key_bytes = bytes(key, encoding='utf-8')
            value_bytes = bytes(value, encoding='utf-8')
            producer_instance.send(topic_name, key=key_bytes, value=value_bytes)
            producer_instance.flush()
        except Exception as ex:
            self.logger.error('Exception in publishing message')
            error = str(ex)
            self.logger.error("Exception occurred", exc_info=True)
        return error

    def connect_kafka_producer(self):
        """
        connect with kafka producer
        :return: kafkaproducer object
        """
        _producer = None
        try:
            _producer = KafkaProducer(bootstrap_servers=['moped-01.srvs.cloudkafka.com:9094',
                                                         'moped-02.srvs.cloudkafka.com:9094',
                                                         'moped-03.srvs.cloudkafka.com:9094'],
                                      security_protocol='SASL_SSL',
                                      sasl_mechanism='SCRAM-SHA-256',
                                      sasl_plain_username='u518r2qy',
                                      sasl_plain_password='xUTDBhfZ-DlmPmRwQ4J1Qw49QsMzieZV',
                                      api_version=(0, 10))

        except Exception as ex:
            self.logger.error('Exception while connecting Kafka')
            print(str(ex))
            self.logger.error("Exception occurred", exc_info=True)
        return _producer

    def fetch_data(self):
        """
        this method fetches the data from google sheet and return it as raw_data and also send tag
        """
        error = None
        tags = None
        try:
            range_name = self.config['SHEETNAME']
            # call class method which return sheet data and error if permission is not there
            get_value_mapping = self.get_sheetvalues(self.config['SHEETID'], range_name)

            mapping_error = get_value_mapping[1]  # Error in fetching mapping
            mapping_values = get_value_mapping[0]  # mapping values list
            if not mapping_error:
                raw_data = mapping_values
                # Create a JSON from data.
                column_names = raw_data[0]
                for data in raw_data[2:]:
                    single_data = dict()
                    counter = 0
                    for col in column_names:
                        if col != '':
                            single_data[col] = data[counter]
                        counter += 1
                    tags = self.get_tags()
                    all_data = dict()
                    all_data['req_data'] = single_data
                    all_data.update(self.config)  # merge tags with sheet each row data
                    raw_data = dict()
                    raw_data['reqd_data'] = all_data
                    raw_data['tags'] = tags
                    kafka_producer = self.connect_kafka_producer()
                    value = json.dumps(raw_data)
                    error = self.publish_message(kafka_producer, 'form-data', 'form-data', value)

            else:
                error = "No Mapping details found"

        except Exception as ex:
            error = "Failed to fetch mapping detials"
            mapping_values = None
            self.logger.error("Exception occurred", exc_info=True)
        return error

    def fetch_mapping(self, data):
        """
        this method fetches mapping values and options from google sheet and update this in raw_data
        return it as raw_data
        """
        error = None
        raw_data = None
        try:
            self.raw_data = data
            self.get_tags()
            info_log(self.logger.info, "Step3 Fetch Mapping Start", self.raw_data)
            get_value_mapping = self.get_sheetvalues(data['SHEETID'], data['MAPPINGDETAILS'])
            mapping_error = get_value_mapping[1]  # Error in fetching mapping
            mapping_values = get_value_mapping[0]  # mapping values list
            get_options_mapping = self.get_sheetvalues(data['SHEETID'],
                                                       data['OPTIONSSHEET'])
            options_error = get_options_mapping[1]  # Error in fetching options
            options_mapping = get_options_mapping[0]  # options mapping list

            if not mapping_error and not options_error:
                raw_data = dict()
                raw_data['value_mapping'] = mapping_values
                raw_data['options_mapping'] = options_mapping
                data.update(raw_data)
                raw_data = data
                self.raw_data = raw_data

            else:
                error = str(mapping_error) + str(options_error)
            info_log(self.logger.info, "Step3 Fetch Mapping End", self.raw_data)

        except Exception as ex:
            error = "Failed to fetch mapping detials"
            info_log(self.logger.error, "Error1 "+error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        return raw_data, error

    def _map_data(self, all_data, mapping_values, options_mapping):
        error = None
        final_data = None
        try:
            info_log(self.logger.info, "Step4.1 Mapping Start", self.raw_data)
            mapping_values.pop(0)  # removing the header row of mapping sheet
            final_data = []  # List to hold the final values
            options_mapping.pop(0)  # removing the header row of options sheet
            for row in mapping_values:
                if row[1] == 'options':
                    # row[2] option value name
                    # str(all_data[row[2]]) option value a,b,c,d
                    # options_mapping[] the list with valuename and options value
                    this_list = ''.join(
                        str(opt) for opt in options_mapping)  # Converted list to string
                    new_list = this_list.split(str(
                        row[2]), 1)[1]  # List split to start with required string
                    index_end = new_list.find("]")  # Find the stopping point
                    # The semi final string to find values from obtained
                    str_to_check = new_list[:
                                            index_end]
                    option_value_start = str_to_check.find(str(all_data[row[2]]))
                    if option_value_start == -1:
                        all_data[row[
                            2]] = 'NO_TEXT_FOUND'  # If the particular option is not found
                        # Appending the received data to the final list
                        final_data.append(all_data[row[2]])
                    else:
                        length = len(all_data[row[2]])
                        option_value_end = str_to_check.find("'", option_value_start)
                        option_value = str_to_check[option_value_start + length + 2:
                                                    option_value_end]
                        final_data.append(
                            option_value
                        )  # Appending the correct option to the final list
                else:
                    if not all_data[row[2]]:
                        all_data[row[2]] = 'NO_TEXT_FOUND'  # If data is None

                    final_data.append(all_data[row[
                        2]])  # Appending the received data to the final list
            info_log(self.logger.info, "Step4.1 Mapping End", self.raw_data)

        except Exception as ex:
            error = "Failed to map data"
            info_log(self.logger.error, "Error3 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        return final_data, error

    def get_config(self):
        """
        return config
        """
        return self.config

    def _generate_file_drive(self, url):
        error = document_id = file_name = pdf_url = None
        try:
            info_log(self.logger.info, "Step4.2 Generate File Drive Start", self.raw_data)
            # call the app script url
            contents = requests.get(url, timeout=60).json()
            print(contents)
            if contents.get("error") != "null":
                error = contents.get('error')
            if error == "undefined":
                error = None
            document_id = contents.get("documentId")
            file_name = contents.get("fileName")
            pdf_url = contents.get("url")
            info_log(self.logger.info, "Step4.2 Generate File Drive End", self.raw_data)

        except Exception as ex:
            error = "Failed to get response from App Script"
            info_log(self.logger.error, "Error4 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)

        return document_id, file_name, pdf_url, error

    def build_pdf(self, raw_data, file_name):
        """
        this method get raw_data and file name and generate pdf having this file_name
        """
        error = None
        pdf_name = ''
        pdf_url = ''
        try:
            data = raw_data['req_data']
            info_log(self.logger.info, "Step4 Build Pdf Start", self.raw_data)
            mapping_values = raw_data['value_mapping']
            options_mapping = raw_data['options_mapping']
            mapped_data = self._map_data(data, mapping_values, options_mapping)
            mapping_error = mapped_data[1]
            final_data = mapped_data[0]
            if not mapping_error:
                # URL of google app script
                final_data_str = json.dumps(final_data)
                if 'FILENAMEFIELD' in raw_data and raw_data['FILENAMEFIELD'] in data:
                    file_name = data[raw_data['FILENAMEFIELD']] + '_' + str(
                        calendar.timegm(time.gmtime()))
                print(file_name)
                payload = {
                    "fileName": file_name,
                    "mylist": final_data_str,
                    "templateId": raw_data['DOCTEMPLATEID']
                }  # Encoding the url with payload
                if ('ODKUSERNAME' in self.raw_data.keys() and self.raw_data['ODKUSERNAME']
                        and 'ODKPASSWORD' in self.raw_data.keys() and self.raw_data['ODKPASSWORD']):
                    call_session_cookie = self._get_session_cookie()

                    if not call_session_cookie[0]:
                        session_cookie = call_session_cookie[1]
                    else:
                        error = call_session_cookie[0]

                    if not error:
                        payload['sessionCookie'] = session_cookie
                        payload['username'] = self.raw_data['ODKUSERNAME']
                        payload['password'] = self.raw_data['ODKPASSWORD']
                if not error:
                    gas_url = self.config['URL'] + urlencode(payload)
                    # Calling the GAS url and Getting the GAS response
                    app_script_response = self._generate_file_drive(gas_url)
                    error = app_script_response[3]

                    if not error:
                        pdf_url = app_script_response[2]
                        pdf_name = app_script_response[1] + '.pdf'

            else:
                error = mapping_error
            info_log(self.logger.info, "Step4 Build Pdf End", self.raw_data)

        except Exception as ex:
            error = "Failed to generate pdf"
            info_log(self.logger.error, "Error2 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        return pdf_name, error, pdf_url

    def upload_pdf(self, key, file_url):
        """
        Uploads a file to the local server and if we specify UPLOADTO in config file then save this
        file to cdn and delete file from local server.
        """
        error = ''
        upload_file_url = None
        expire_timestamp = None
        try:
            info_log(self.logger.info, "Step5 Upload Pdf Start", self.raw_data)
            response = requests.get(file_url)
            base_path = os.path.dirname(__file__) + self.config['DIRPATH']
            if not os.path.exists(base_path):
                os.makedirs(base_path)
            with open(base_path + key, 'wb') as file_obj:
                file_obj.write(response.content)
                upload_file_url = base_path + key
                base_path = os.path.dirname(__file__)
                if ('UPLOADTO' in self.config.keys() and self.config['UPLOADTO']):
                    info_log(self.logger.info, "Step5.1 Upload To Cdn Start", self.raw_data)
                    if self.config['UPLOADTO'] == 's3':
                        cdn_upload = FileUploader(self.config['UPLOADTO'], self.config['ACCESSKEY'],
                                                  self.config['SECRETKEY'])
                    else:
                        cdn_upload = FileUploader(self.config['UPLOADTO'],
                                                  base_path + '/' +
                                                  self.config['GOOGLE_APPLICATION_CREDENTIALS'])
                    resp = cdn_upload.upload_file(base_path + self.config['DIRPATH'] + key,
                                                  self.config['BUCKET'], key)
                    url = resp[0]
                    error = resp[1]
                    if url:
                        upload_file_url = url
                        expire_timestamp = resp[2]
                        os.remove(os.path.dirname(__file__) + self.config['DIRPATH'] + key)
                    else:
                        info_log(self.logger.error, "Error6 " + error, self.raw_data)

                    info_log(self.logger.info, "Step5.1 Upload To Cdn End", self.raw_data)

            #self._delete_file_drive(file_url)
            info_log(self.logger.info, "Step5 Upload Pdf End", self.raw_data)

        except Exception as ex:
            error = "Failed to download file from drive"
            info_log(self.logger.error, "Error5 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        return upload_file_url, error, expire_timestamp

    def retrieve_pdf(self, key):
        """
        this method return pdf url
        """
        filedata = ''
        error = None
        file_name = self.config['DIRPATH'] + key + '.pdf'
        try:
            with open(file_name, 'rb') as file_obj:
                filedata = file_obj.read()
        except Exception as ex:
            error = 'File not found'
            self.logger.error("Exception occurred", exc_info=True)
        return filedata, error

    def _delete_file_drive(self, file):
        """
        Google drive API to Permanently delete a file, skipping the trash.
        """
        error = done = None
        try:
            creds = None
            creds = self._get_token()[1]
            service = build('drive', 'v3', credentials=creds)
            doc_id = file.split('/')
            file_id = doc_id[5]  # find file id from url here
            service.files().delete(fileId=file_id).execute()
            done = True

        except Exception as ex:
            error = 'Failed to delete file'
            print(ex)
            self.logger.error("Exception occurred", exc_info=True)
        return error, done

    def delete_file_drive_google_script(self, file):
        """
        Trash Google drive file using google app script.
        """
        error = done = None
        try:
            #fileId = '1Bk48xG8buQu6Y1z7QlXc-GffRwoRsR3ciDb7aeTQQMo'
            payload = {
                "fileId": file
            }
            url = self.config['DRIVE_DELETE_URL']
            gas_url = url + urlencode(payload)
            contents = requests.get(gas_url, timeout=60).json()
            print(contents)
            if contents.get("error") != "null":
                error = contents.get('error')
            if error == "undefined":
                error = None
            if error:
                self.logger.error("Error occurred in delete file drive " + error)
            else:
                done = True
        except Exception as ex:
            error = 'Failed to delete file'
            print(ex)
            self.logger.error("Exception occurred", exc_info=True)
        return error, done


    def shorten_url(self, url, doc_url):
        """
        Generate short url
        :param url:
        :return:
        """
        info_log(self.logger.info, "Step6 Shorten Url Start", self.raw_data)
        short_url = None
        error = None
        api_key = self.config['POLRACCESSTOKEN']
        try:
            querystring = {"key": api_key,
                           "url": url}
            resp = requests.request("GET", self.config['POLRAPIURL'], params=querystring)
            if resp.status_code == 200:
                short_url = resp._content.decode("utf-8")
                tags = self.get_tags()
                new_doc_url = doc_url.replace('export?format=pdf', 'edit')
                print(new_doc_url)
                if 'SENDMSG' in self.config[tags["FORMID"]].keys() and \
                        self.config[tags["FORMID"]]['SENDMSG']:
                    info_log(self.logger.info, "Step6.2 Msg Send Start", self.raw_data)

                    raw_data = self.raw_data
                    req_data = raw_data['req_data']
                    name = req_data[self.config[tags["FORMID"]]['NAMEFIELD']]
                    mobile = req_data[self.config[tags["FORMID"]]['MSGFIELD']]
                    print(name)
                    print(mobile)
                    # req_data = raw_data['req_data']
                    msg_result = send_whatsapp_msg(mobile,
                                                   url,
                                                   name, new_doc_url)
                    info_log(self.logger.info, "Step6.2 Msg Send End", self.raw_data)
                    msg_error = msg_result[0]
                    msg_resp = msg_result[1]
                    if msg_error:
                        error = msg_error
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                                raw_data['INSTANCEID'] and raw_data['FORMID']:
                            self.logger.error(
                                "Step6.2 Send Msg Error %s - instance id %s - Form id %s",
                                msg_resp.__dict__,
                                raw_data['INSTANCEID'], raw_data['FORMID'])
                    info_log(self.logger.info, "Step6.2 Msg Send End", self.raw_data)

                if 'SENDEMAIL' in self.config[tags["FORMID"]].keys() and \
                        self.config[tags["FORMID"]]['SENDEMAIL']:
                    info_log(self.logger.info, "Step6.3 Email Send Start", self.raw_data)

                    raw_data = self.raw_data
                    req_data = raw_data['req_data']
                    name = req_data[self.config[tags["FORMID"]]['NAMEFIELD']]
                    email = req_data[self.config[tags["FORMID"]]['EMAILFIELD']]
                    template_id = self.config[tags["FORMID"]]['EMAILTEMPLATEID']
                    print(name)
                    print(email)
                    custom_fields = {'FULL_NAME': name, "LINK": url, "DOC_LINK": new_doc_url}
                    # req_data = raw_data['req_data']
                    mail_result = send_mail(email,
                                            url, custom_fields,
                                            'resume', template_id)
                    mail_error = mail_result[0]
                    mail_resp = mail_result[1]
                    if mail_error:
                        if all(raw_key in raw_data for raw_key in ("INSTANCEID", "FORMID")) and \
                                raw_data['INSTANCEID'] and raw_data['FORMID']:
                            self.logger.error(
                                "Step6.2 Email Send Error %s - instance id %s - Form id %s",
                                mail_resp.__dict__,
                                raw_data['INSTANCEID'], raw_data['FORMID'])
                        if error:
                            error += mail_error
                        else:
                            error = mail_error
                    info_log(self.logger.info, "Step6.3 Email Send End", self.raw_data)

            else:
                error = resp._content.decode("utf-8")
                info_log(self.logger.error, "Error7 " + error, self.raw_data)
            info_log(self.logger.info, "Step6 Shorten Url End", self.raw_data)

        except Exception as ex:
            error = "Unable to shorten a url"
            info_log(self.logger.error, "Error7 " + error, self.raw_data)
            self.logger.error("Exception occurred", exc_info=True)
        return short_url, error
