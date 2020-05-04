"""
Plugin for getting data from another server and generate pdf from it
"""
import json
import os.path
from flask import request
from queuelib import FifoDiskQueue
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
        with open(os.path.dirname(__file__) + '/config.json') as json_file:
            config = json.load(json_file)
            self.config = config
        self.raw_data = None

    def get_tags(self):
        """
        this method return all the tags on the basis of which we filter the request
        """
        tags = dict()
        tags["SHEETID"] = self.config["SHEETID"]
        tags["MAPPINGDETAILS"] = self.config["MAPPINGDETAILS"]
        tags["OPTIONSSHEET"] = self.config["OPTIONSSHEET"]
        tags["DOCTEMPLATEID"] = self.config["DOCTEMPLATEID"]
        tags["APPLICATIONID"] = self.config["APPLICATIONID"]
        if self.raw_data:
            tags["FORMID"] = self.raw_data["FORMID"]
            tags["USERNAME"] = self.raw_data["USERNAME"]
            tags["FORMSUBMISSIONDATE"] = self.raw_data["FORMSUBMISSIONDATE"]
            tags["INSTANCEID"] = self.raw_data["INSTANCEID"]
        return tags

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

            new_req_data = json.loads(json.dumps(new_req_data))  # Getting the new data
            user_name = new_req_data['username']
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
                        req_val = "NO_TEXT_FOUND"

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
            queue_data = FifoDiskQueue(os.path.dirname(__file__)+'/../../queuedata')
            queue_data.push(json.dumps(raw_data).encode('utf-8'))
            queue_data.close()
        except Exception as ex:
            error = "Failed to fetch mapping detials"

        return error
